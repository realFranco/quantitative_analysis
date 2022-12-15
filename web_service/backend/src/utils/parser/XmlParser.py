from typing import List
import xml.dom.minidom

from src.models.ArchimateElement import ArchimateElement
from src.models.ArchimateValidConcepts import ArchimateValidConcepts

class XmlArchimateConcepts:

    archiDiagram = '../../resources/archi_diagram_example/healthcare.archimate'

    @staticmethod
    def collectBusinessService(concept: str = 'BusinessRole', diagram: str = None) -> List[ArchimateElement]:
        if False == ArchimateValidConcepts.has_value(concept):
            return []

        doc = xml.dom.minidom.parse(
            file=XmlArchimateConcepts.archiDiagram if not diagram else \
                XmlArchimateConcepts.archiDiagram.replace('healthcare.archimate', diagram)
        )
        element = doc.getElementsByTagName("element")
        targetType = f'archimate:{concept}'
        return [ArchimateElement(id=el.getAttribute('id'), name=el.getAttribute('name'))
            for el in element if el.getAttribute('xsi:type') == targetType]
