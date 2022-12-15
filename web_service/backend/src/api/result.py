"""
Result router.
"""
import os
import datetime
import json
import traceback
from pathlib import Path
import re

from fastapi import APIRouter, Response

from src.config.Routes import Routes
from src.config.Tags import Tags
from src.config.Messages import Messages


result = APIRouter(
    prefix=Routes.RESULT,
    tags=[Tags.result],
    responses={404: Messages.NOT_FOUND}
)

@result.get('/collect')
async def collect_result(toCsv: bool = False, simulationFile: str = None):
    try:
        content: dict = {}

        csvContent: str = None
        fileToRead: str = None

        if simulationFile == None:
            files = sorted(Path('../../resources/').iterdir(), key=lambda f: f.stat().st_mtime)
            files = [str(f) for f in files if 'jArchiQuantitativeAnalysisResults.json' in str(f)]
            fileToRead = files[-1]
        else:
            # Case when the endpoint need to retrieve a specific `json` file as results. The file it's
            # passed on the endpoint through the argument `simulationFile`.
            fileToRead = f'../../resources/{simulationFile}'

        # The last file is the most recent modified file.
        with open(fileToRead, 'r') as f:
            content = json.loads(f.read())
            f.close()

        if toCsv == True:
            csvContent = ', '.join(content[0].keys()) + '\n'

        # Logic: Reduce the decimals to show.
        for row in content:
            row['work'] = float(format(float(row['work']), '.2f'))
            row['cost'] = float(format(float(row['cost']), '.2f'))

            if toCsv == True:
                csvContent += ', '.join([str(v) for v in row.values()]) + '\n'

        return content if csvContent == None else csvContent

    except Exception as error:
        print('At collect result.')
        traceback.print_exc()

        return {
            'errorMessage': str(error)
        }


@result.get('/collect/heat-map-reference')
async def heat_map_reference(clean: bool = False, reverse: bool = False):
    """
    Return the heat map reference in order to obtain column and row names.

    :param clean bool. 
        - If set in True, the object to return will be exposed as a translate object {key: value}.
        - If set in False, the object to return a list of object, evert object will be used to expose a row
        inside a table.

    :param reverse bool:
        As general rule, only used if the `clean` argument is set to `True`.
        - If set in True, the object to return will be reverse, the keys become values and values become keys.
        This is required to reutilize the same endpoint and return the same data set into different ways.
    """
    def improveSyntaxOnSimulationConcepts(word) -> str:
        word = word[0].capitalize() + word[1:]

        return ' '.join(re.findall('[A-Z][^A-Z]*', word))

    try:
        group = {}
        outGroup = [] if clean == False else {}

        groupCounter = 1
        conceptCounter = 1

        resultFiles = [route for route in os.listdir('../../resources/') 
            if True == ('jArchiQuantitativeAnalysisResults.json' in route)]

        for resultFile in resultFiles:
            _, entryPointConcept, _, _ = resultFile.split('.')
            group[entryPointConcept] = f'S{groupCounter}'

            if clean == False:
                outGroup.append({
                    # 'nombre concepto': entryPointConcept,
                    'nombre concepto': improveSyntaxOnSimulationConcepts(entryPointConcept),
                    'leyenda': f'S{groupCounter}',
                })
            else:
                outGroup[entryPointConcept] = f'S{groupCounter}'

            groupCounter += 1

        with open(f'{os.getenv("PROJECT_LOCATION")}resources/{resultFiles[0]}', 'r') as f:
            resultsData = json.loads(f.read())
            for row in resultsData:
                group[row['name']] = f'C{conceptCounter}'
                if clean == False:
                    outGroup.append({
                        'nombre concepto': row['name'],
                        'leyenda': f'C{conceptCounter}',
                    })
                else:
                    outGroup[row['name']] = f'C{conceptCounter}'

                conceptCounter += 1
            f.close()

        if True == clean and True == reverse:
            outGroup = dict(zip(outGroup.values(), outGroup.keys()))

        return outGroup

    except Exception as error:
        print('At heat map reference')
        traceback.print_exc()

        return {
            'errorMessage': str(error)
        }

@result.get('/collect/higher-visited-concept')
async def higher_visited_concept() -> int:
    try:
        higherVisitedConcept = 0
        for resultFile in os.listdir('../../resources/'):
            if True == ('jArchiQuantitativeAnalysisResults.json' in resultFile):
                with open(f'{os.getenv("PROJECT_LOCATION")}resources/{resultFile}', 'r') as f:
                    resultsData = json.loads(f.read())
                    for row in resultsData:
                        if higherVisitedConcept < row['visited']:
                            higherVisitedConcept = row['visited']

        return higherVisitedConcept

    except Exception as error:
        print('At higher visited concept')
        traceback.print_exc()

        return {
            'errorMessage': str(error)
        }

@result.get('/collect/heat-map')
async def collect_heat_map():
    try:
        # Logic:  Return a List of `HeatMapRow`.
        out = []

        # Ubicar el valor `visited` más alto en todas silumaciones.
        higherValue = await higher_visited_concept();

        for resultFile in os.listdir('../../resources/'):
            # print(f'resultFile: {resultFile}')
            if True == ('jArchiQuantitativeAnalysisResults.json' in resultFile):
                _, entryPointConcept, _, _ = resultFile.split('.')
                # print(f'projectName: {projectName}')
                # print(f'entryPointConcept: {entryPointConcept}')

                with open(f'{os.getenv("PROJECT_LOCATION")}resources/{resultFile}', 'r') as f:
                    resultsData = json.loads(f.read())
                    for row in resultsData:
                        out.append(
                            {
                                'group': row['name'],
                                'variable': entryPointConcept,
                                'value': row['visited'] / higherValue * 100,
                            }
                        )
                    f.close()

        translateObject = await heat_map_reference(clean=True)

        # Json to Csv
        csvContent = ''
        if out:
            csvContent = ','.join(out[0].keys()) + '\n'
            for row in out:
                # Translate the elements to be displayed into the Heat Map
                values = [translateObject[val] for val in row.values() if val in translateObject]
                values.append(row['value'])
                csvContent += ','.join([str(v) for v in values]) + '\n'

        return Response(content=csvContent, media_type="text/plain; charset=utf-8")
    
    except Exception as error:
        print('At collect heat map.')
        traceback.print_exc()

        return {
            'errorMessage': str(error)
        }

@result.get('/collect/simulation-historical')
async def collect_simulation_historical():
    try:
        simulationResultDirectory = '../../resources/'
        out = []

        def upperFirstLetter(word: str) -> str:
            return word[0].capitalize() + word[1:]

        for resultFile in os.listdir(simulationResultDirectory):
            if True == ('jArchiQuantitativeAnalysisResults.json' in resultFile):
                fileName = f'{simulationResultDirectory}{resultFile}'
                modificationTimestamp = os.path.getmtime(fileName)

                simulationName = upperFirstLetter(resultFile.split('.')[1])
                capitalizedSimulationName = ' '.join(re.findall('[A-Z][^A-Z]*', simulationName))

                out.append(
                    {
                        'file': capitalizedSimulationName,
                        'realFileName': resultFile,
                        'date': int(modificationTimestamp),
                        'humanizeDate': datetime.datetime.fromtimestamp(modificationTimestamp)
                            .strftime('%d/%m/%y %H:%M')
                    }
                )

        # Return a sort list of dictionaries based on the `date` property.
        return sorted(out, key=lambda d: d['date'], reverse=True)  if out else out

    except Exception as error:
        print('At collect simulation historical')
        traceback.print_exc()

        return {
            'errorMessage': str(error)
        }

@result.delete('/delete-simulations')
async def delete_simulations():
    try:
        deletes: int = 0
        simulationResultDirectory = '../../resources/'
        for resultFile in os.listdir(simulationResultDirectory):
            if True == ('jArchiQuantitativeAnalysisResults.json' in resultFile):
                print(f'file to remove: {resultFile}')
                os.remove(f'{simulationResultDirectory}{resultFile}')
                deletes += 1

        return {
            'message': 'Files deleted',
            'deletes': deletes 
        }

    except Exception as error:
        print('At delete simulations')
        traceback.print_exc()

        return {
            'errorMessage': str(error)
        }
