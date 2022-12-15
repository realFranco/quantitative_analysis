/**
 * Service to expose the grid.
 * 
 * https://www.ag-grid.com/javascript-data-grid/getting-started/
 */

const apiUrl = 'http://127.0.0.1:8000';

const archimateColorYellow = '#ffffb5';
const archimateColorBlue = '#b5ffff';
const archimateColorGreen = '#c9e7b7';

const archimateColorForNodeType = {
    'business-service': archimateColorYellow,
    'business-role': archimateColorYellow,
    'business-process': archimateColorYellow,
    'application-service': archimateColorBlue,
    'application-component': archimateColorBlue,
    'technology-service': archimateColorGreen,
    'device': archimateColorGreen
}

const translateKeySpanish = {
    'work': 'Carga de Trabajo',
    'cost': 'Rendimento',
    'visited': 'Visitado',
    'name': 'Nombre',
    'type': 'Tipo',
}

var exposeArchiResults = document.getElementById('exposeArchiResults');
var exposeArchiResultsHeatMap = document.getElementById('exposeArchiResultsHeatMap');


// Given the endpoint response enable the heat map display.
// If the endpoint return data, display or hide the heap by demand.
function isResultHeatMapValidToExpose(data) {
    return data !== '' ? true : false;
}

function showHideObject(object) {
    if (object.style.display === '') {
        object.style.display = 'none';
    } else if (object.style.display === 'none') {
        object.style.display = '';
    }
}

// Show | Hide the result grids, the table and the heat map.
function exposeResultGrid() {
    showHideObject(exposeArchiResults);
    loadHeatMap();
}

// Given a list of objects, return the properties from one of the objects.
function getColumnDefinition(data) {
    var out = [];

    if (0 === data.length){
        return out;
    }

    var keys = Object.keys(data[0]);

    for(var index = 0; index < keys.length; index++){
        let row = { field: keys[index] }

        if (true === translateKeySpanish.hasOwnProperty(keys[index])) {
            row['headerName'] = translateKeySpanish[keys[index]];
        }

        // Sorting see: https://www.ag-grid.com/javascript-data-grid/row-sorting/
        if ('work' === keys[index] || 'cost' === keys[index] || 'visited' === keys[index]) {
            row['comparator'] = (valueA, valueB, nodeA, nodeB, isDescending) => valueA - valueB

            if ('work' === keys[index]) {
                row['width'] = 150;
            } else if ('cost' === keys[index]) {
                row['width'] = 115;
            } else if ('visited' === keys[index]) {
                row['width'] = 100;
                row['resizable'] = false;
            }

        } else if ('name' === keys[index]) {
            row['comparator'] = (valueA, valueB, nodeA, nodeB, isDescending) => {
                if (valueA == valueB) return 0;
                return (valueA > valueB) ? 1 : -1;
            }

            row['width'] = 290;

        } else if ('type' === keys[index]) {
            // TODO: La columna `type` tiene un orden en particular
            // business, application, technology | business > technology
            // Improve sorting
            row['comparator'] = (valueA, valueB, nodeA, nodeB, isDescending) => {
                if (valueA.includes('business') && valueB.includes('application')) return 1;
                if (valueA.includes('application') && valueB.includes('technology')) return 0;
                return -1;
            }
        } else if ('nombre concepto' == keys[index]) {
            row['width'] = 300;
        }
        out.push(row)
    }

    return out;
}

function colorRepresentation(row) {
    // console.log('params data type ', row.data.type);
    if (false === archimateColorForNodeType.hasOwnProperty(row.data.type)){
        return {};
    }

    return {
        backgroundColor: archimateColorForNodeType[row.data.type],
    };
}

function getGridOptions(data) {
    return {
        defaultColDef: {
            sortable: true,
            resizable: true,
        },
        columnDefs: getColumnDefinition(data),
        rowData: data,
        getRowStyle: (params) => {
            return colorRepresentation(params);
        },
    };
}

function getGridOptionsClean(data) {
    return {
        defaultColDef: {
            sortable: true,
            resizable: true,
        },
        columnDefs: [
            { field: 'file', headerName: 'Nodo Inicial', width: 175 },
            { field: 'humanizeDate', headerName: 'Fecha de Simulación', width: 165 },
        ],
        rowData: data,
        onRowClicked: (event) => {
            // Send the event.data into the `loadNormalGrid()` function in order to render one more time the grid
            loadNormalGrid(event.data);
            
            // Use the `localStorage` in order to store data required in future steps.
            // When the user click on a row at the "history of simulations" table, the `onRowClicked` event will be
            // triggered.
            // That particular event will be useful in order to set a local object into the web browser.
            // Also, when the `onBtnExport()` is called the `localStorage` object will request the 
            // `jArchiSimulationNodeName` value.
            localStorage.setItem('jArchiSimulationNodeName', event.data.realFileName);
        },
    }
}

function onBtnExport() {
    // Hit an endpoint that return .csv file.

    if (null === localStorage.getItem('jArchiSimulationNodeName')){
        // If there is not a key `jArchiSimulationNodeName` inside `localStorage` don't perform the download action.
        return;
    }

    var simulationFile = (null === localStorage.getItem('jArchiSimulationNodeName')) 
        ? ''
        : `&simulationFile=${localStorage.getItem('jArchiSimulationNodeName')}`;

    fetch(`${apiUrl}/result/collect?toCsv=true${simulationFile}`, {method: 'GET'})
        .then((response) => response.json())
        .then(response => {
            // Add a name into the CSV file to download. The filename will depends on the most recent node clicked.
            // If no local value it's store for the key `jArchiSimulationNodeName` a default name will be used.
            var filename = ('' !== simulationFile) 
                ? localStorage.getItem('jArchiSimulationNodeName').replace('.json','.csv').split('.').slice(1,4).join('.')
                : 'jArchiQuantitativeAnalysisResults.csv';

            let element = document.createElement('a');

            element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(response));
            element.setAttribute('download', filename);
            element.style.display = 'none';
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);

        })
        .catch(response => {
            console.log('Error at `onBtnExport` ', response);
        });
}

// Fetch data from one endpoint and render the table.
// Also, contains another responsibility, export the the data as a Csv format.
// externalData: Object {date, file, humanizeDate, realFileName}
function loadNormalGrid(externalData) {
    var simulationFile = (undefined !== externalData) ? `?simulationFile=${externalData.realFileName}` : "";

    fetch(`${apiUrl}/result/collect${simulationFile}`, {method: 'GET'})
        .then((response) => response.json())
        .then((response) => {
            var gridOptions = getGridOptions(response);

            // If there is a defined `simulationFile` argument, fetch new data from the API & draw new nodes.
            if (undefined !== externalData) {
                // Remove all the grid.
                const resultGrid = document.getElementById("archimateTableResultGrid");
                resultGrid.innerHTML = '';
                
                // Re-render the grid.
                const gridDiv = document.querySelector('#archimateTableResultGrid');
                new agGrid.Grid(gridDiv, gridOptions);
            }
            else {
                // Setup the grid after the page has finished loading.
                document.addEventListener('DOMContentLoaded', () => {
                    const gridDiv = document.querySelector('#archimateTableResultGrid');
                    new agGrid.Grid(gridDiv, gridOptions);
                });
            }
        })
        .catch(response => {
            console.log('`loadNormalGrid` raise an error.');
            console.log(response);
        });
}

// Fetch data from one endpoint and render a table.
// If the argument `isActionReload` it's passed, the grid will be reloaded in order to render changes.
function loadSimulationGrid(isActionReload) {
    fetch(`${apiUrl}/result/collect/simulation-historical`, {method: 'GET'})
        .then((response) => response.json())
        .then((response) => {
            var gridOptions = getGridOptionsClean(response);

            if (undefined !== isActionReload) {

                // Remove all the grid.
                const resultGrid = document.getElementById("archimateTableSimulation");
                resultGrid.innerHTML = '';

                const gridDiv = document.querySelector('#archimateTableSimulation');
                new agGrid.Grid(gridDiv, gridOptions);
            } else {
                // Setup the grid after the page has finished loading.
                document.addEventListener('DOMContentLoaded', () => {
                    const gridDiv = document.querySelector('#archimateTableSimulation');
                    new agGrid.Grid(gridDiv, gridOptions);
                });
            }
        })
        .catch((response) => {
            console.log('`loadSimulationGrid` raise an error.');
            console.log(response);
        });
}

// Fetch data from and endpoint and render a legend table that act as a reference.
function loadNormalReferenceGrid() {
    fetch(`${apiUrl}/result/collect/heat-map-reference`, {method: 'GET'})
        .then((response) => response.json())
        .then((response) => {
            var gridOptions = getGridOptions(response);
            gridOptions.defaultColDef.resizable = false;
            
            const resultGrid = document.getElementById("archimateTableResultLegendGrid");
            resultGrid.innerHTML = '';
            
            const gridDiv = document.querySelector('#archimateTableResultLegendGrid');
            new agGrid.Grid(gridDiv, gridOptions);

            // Setup the grid after the page has finished loading.
            // document.addEventListener('DOMContentLoaded', () => {
            //     const gridDiv = document.querySelector('#archimateTableResultLegendGrid');
            //     new agGrid.Grid(gridDiv, gridOptions);
            // });
        })
        .catch(response => {
            console.log('`loadNormalReferenceGrid` raise an error.');
            console.log(response);
        });
}


// Fetch data from one endpoint and render a heat map whenever it is possible.
function loadHeatMap() {
    fetch(`${apiUrl}/result/collect/heat-map`, {method: 'GET'})
        .then(response => {
            
            // Determinar si la data es válida.
            if (true == isResultHeatMapValidToExpose(response)){
                // Determinar si el grid está oculto para activarlo o viceversa.
                showHideObject(exposeArchiResultsHeatMap);
            }
        })
        .catch(response => {
            console.log('`exposeResultGrid` raise an error.');
            console.log(response);
        });
}

function cleanSimulations() {

    // Endpoint para borrar los json files de simulaciones.
    fetch(`${apiUrl}/result/delete-simulations`, {method: 'DELETE'})
        .then((response) => response.json())
        .then(() => {
            const resultSimulationGrid = document.getElementById("archimateTableSimulation");
            resultSimulationGrid.innerHTML = '';
            
            const resultGrid = document.getElementById("archimateTableResultGrid");
            resultGrid.innerHTML = '';
            
            resultContainerToExpose(false);

            const exposeResultButton = document.getElementById("executeExposeResultModalButton");
            exposeResultButton.setAttribute('disabled', '');

        })
        .catch((response) => {
            console.log('`cleanSimulations` raise an error.');
            console.log(response);
        });
}

// Will check if exits simulations results in `json` format.
// If so the `executeExposeResultModalButton` will be enable, otherwise disabled.
function isSimulationsResultsAvailable() {
    const exposeResultButton = document.getElementById("executeExposeResultModalButton");
    
    fetch(`${apiUrl}/result/collect/simulation-historical`, {method: 'GET'})
    .then((response) => response.json())
    .then((response) => {
        if (response.length > 0) {
                loadNormalGrid();
                loadSimulationGrid();
                loadNormalReferenceGrid();

                exposeHeatMapRender();
                
                exposeResultButton.removeAttribute('disabled');
                
                resultContainerToExpose(true);

            } else if (response.length <= 0) {
                exposeResultButton.setAttribute('disabled', '');

                resultContainerToExpose(false);
            }
        })
        .catch((response) => {
            console.log('`isSimulationsResultsAvailable` raise an error');
            console.log(response);
        })
}

/**
 * Function to help during the result visualization.
 * 
 * All the tables will be contained by a `div`, use this function to enable or disable the attribute `disabled` in
 * order to expose the content.
 * 
 * @param {boolean} expose `true`: means the result container will be visualized, `false` means the result container 
 * will be hide.
 */
function resultContainerToExpose(expose) {
    const resultArtifacts = document.getElementById("resultArtifacts");

    if (true === expose) {
        resultArtifacts.removeAttribute('style');
    } else if (false === expose) {
        resultArtifacts.setAttribute('style', 'display: none;');
    }
}

function main() {
    // console.log('Expose Quantitative Analysis simulation results.');
    loadNormalGrid();
    loadSimulationGrid();
    loadNormalReferenceGrid();
}

main();
