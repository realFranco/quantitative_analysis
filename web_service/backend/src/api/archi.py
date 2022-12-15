"""
Archi router.
"""
import os
import traceback

from fastapi import APIRouter

from src.config.Routes import Routes
from src.config.Tags import Tags
from src.config.Messages import Messages
from src.utils.ArchiStatus import ArchiStatus
from src.utils.ArchiRunner import ArchiRunner
from src.utils.parser.XmlParser import XmlArchimateConcepts
from src.utils.ScriptConfig import ScriptConfig
from src.models.ArchimateConcept import ArchimateConcept
from src.utils.RemoveAccent import RemoveAccent


archi = APIRouter(
    prefix=Routes.ARCHI,
    tags=[Tags.archi],
    responses={404: Messages.NOT_FOUND},
)

@archi.get('/check-service', tags=[Tags.archi])
async def check_service():
    """Check if the "Archi" service is already running."""
    try:
        print('Executing `Archi.check_service` method.')
        return ArchiStatus.check_service()
    
    except Exception as error:
        print('At route "archi" and `check_service` endpoint ', error)
        traceback.print_exc()
        return {
            'errorMessage': str(error)
        }


@archi.get('/run-service', tags=[Tags.archi])
async def run_service():
    """Run the "Archi" service."""
    try:
        return ArchiRunner.run_service()
    
    except Exception as error:
        print('At route "archi" and `run_service` endpoint ', error)
        traceback.print_exc()

        return {
            'errorMessage': str(error)
        }


@archi.get('/collect-archi-projects', tags=[Tags.archi])
def collect_archi_projects():
    """Will observe all the `.archimate` files inside the directory `archi_diagram_example/`."""
    try:
        return {
            'archimateProjects': [ project for project in os.listdir('../../resources/archi_diagram_example/')
                if '.archimate' in project and not '.bak' in project]
        }

    except Exception as error:
        print('Collect archi projects ', error)
        traceback.print_exc()

        return {
            'errorMessage': str(error)
        }


@archi.get('/collect-archi-concepts', tags=[Tags.archi])
def collect_archi_concepts(concept: str = 'BusinessRole', diagram: str = None):
    """Collect archi concepts where to run the Quantitative Simulation."""
    try:
        # Enviar el diagrama el cual parsear.
        return XmlArchimateConcepts.collectBusinessService(concept=concept, diagram=diagram)

    except Exception as error:
        print('Collect archi concept ', error)
        traceback.print_exc()

        return {
            'errorMessage': str(error)
        }


@archi.post('/set-initial-archimate-concept', tags=[Tags.archi])
def set_initial_archimate_concept(archimate_concept: ArchimateConcept):
    """
    Edit internal configuration resources in order to set the initial Archimate concept.
    
    Useful to start the Quantitative Analysis algorithm.
    """
    try:
        ScriptConfig.set_property(
            'QUANTITATIVE_ANALYSIS_INITIAL_CONCEPT',
            archimate_concept.concept
        )

        ScriptConfig.set_property(
            'QUANTITATIVE_ANALYSIS_INITIAL_CONCEPT_NORMALIZED',
            RemoveAccent.normalize(archimate_concept.concept)
        )

        return {
            'message': 'Initial Archimate correctly concept set'
        }

    except Exception as error:
        print('Set initial Archimate concept ', error)
        traceback.print_exc()

        return {
            'errorMessage': str(error)
        }
