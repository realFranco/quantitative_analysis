export class ExecuteArchiResourcesModal {
    /**
     * @type {HTMLDivElement}
     */
    modal = document.getElementById('executeArchiResourcesModal');

    /**
     * @type {HTMLInputElement}
     */
    activeTutorialButton = document.getElementById('executeArchiResourcesModalTutorialActiveButton');
    
    /**
     * @type {HTMLButtonElement}
     */
    executeArchiResourcesModalRunButton = document.getElementById('executeArchiResourcesModalRunButton');

    /**
     * @type {HTMLElement}
     */
    inputArchiDiagram = document.getElementById('inputArchiDiagram');

    /**
     * @type {HTMLElement}
     */
    inputArchiConcept = document.getElementById('inputArchiConcept');

    /**
     * @type {HTMLElement}
     */
    executeArchiResourcesModalTutorial = document.getElementById('executeArchiResourcesModalTutorial');

    /**
     * @type {HTMLElement}
     */
    executeArchiExternal = document.getElementById('executeArchiExternal');

    // TODO: cambiar a que apunte a url valida
    // apiUrl = 'localhost:PORT';
    apiUrl = 'http://127.0.0.1:8000';

    constructor() {
        this.initializeListeners();
        this.collectArchiProjects();

        this.collectArchiConcepts(this.inputArchiDiagram.value);
    }

    initializeListeners() {
        this.activeTutorialButton.addEventListener('click', () => {
            if (false === this.activeTutorialButton.checked){
                executeArchiResourcesModalTutorial.style.display = 'none';
            }else{
                executeArchiResourcesModalTutorial.style.display = '';
            }
        });

        this.inputArchiDiagram.addEventListener('click', () => {
            this.collectArchiConcepts(this.inputArchiDiagram.value);
        });

        this.executeArchiResourcesModalRunButton.addEventListener('click', () => {
            this.updateViewToShowFormSuccess();
            if (false === this.formIsValid()) {
                this.disableModalClose();
                this.updateViewToShowFormErrors();
                return;
            }

            this.formValidationError();
            // Guardar el concepto inicial para ejecutar la simulación
            this.setInitialArchiConcept(this.inputArchiConcept.value);

            // Ejecutar endpoint para ejecutar ArchiMate
            this.runArchiService();

            this.cleanInputArchiConceptStyle();
        });

        this.executeArchiExternal.addEventListener('click', () => {
            // Required to set correct style along the Execute Archi modal.
            const executeArchiResourcesModal = document.getElementById('executeArchiResourcesModal');
            executeArchiResourcesModal.setAttribute('style', 'padding-right: 550px; display: block;');
        })
    }

    // Feed the initial projects
    collectArchiProjects() {
        fetch(`${this.apiUrl}/archi/collect-archi-projects`, {
            method: 'GET'
        })
            .then((response) => response.json())
            .then((response) => {
                response.archimateProjects.forEach(item => {
                    let opt = document.createElement('option');
                    opt.value = item;
                    opt.innerHTML = item;
                    this.inputArchiDiagram.appendChild(opt);
                });
            })
    }

    // Feed the initial concepts
    collectArchiConcepts(archimateDiagram) {

        var archimateConcept = 'BusinessRole';
        fetch(`${this.apiUrl}/archi/collect-archi-concepts?concept=${archimateConcept}&diagram=${archimateDiagram}`, {
            method: 'GET'
        })
            .then((response) => response.json())
            .then((response) => {
                inputArchiConcept.innerHTML = '';

                // At the select drop down, add the `option` Html tags.
                var index = 0;
                response.forEach(item => {
                    let opt = document.createElement('option');
                    
                    if (0 === index) {
                        let opt = document.createElement('option');
                        opt.value = 'Selecciona un elemento inicial';
                        opt.innerHTML = 'Selecciona un elemento inicial';
                        inputArchiConcept.appendChild(opt);

                        index += 1;
                    }
                    opt.value = item.name;
                    opt.innerHTML = item.name;
                    inputArchiConcept.appendChild(opt);
                });
            })
            .catch((response) => {
                console.log({ response });
            });
            
    }

    setInitialArchiConcept(archimateConcept) {
        var myHeaders = new Headers();
        myHeaders.append("Content-Type", "application/json");

        var body = JSON.stringify({ "concept": archimateConcept });

        fetch(`${this.apiUrl}/archi/set-initial-archimate-concept?archimate_concept=${archimateConcept}`, {
            method: 'POST',
            headers: myHeaders,
            body: body,
        })
            .then((response) => response.json())
            .then(() => {
                document.getElementById("executeArchiResourcesModalCloseButton").click();

                this.alertEventInformation('¡Archi está en 2do. plano o espere a su ejecución!', 'success');
            })
            .catch((response) => {
                console.log({response});

                document.getElementById("executeArchiResourcesModalCloseButton").click();

                this.alertEventInformation('¡Sucedió un problema al ejecutar Archi!', 'warning');
            });
    }

    // This function will hit an Http Get endpoint in order to execute the Archi application
    runArchiService() {
        fetch(`${this.apiUrl}/archi/run-service`, {
            method: 'GET',
        })
            .then((response) => response.json())
            .catch((response) => {
                console.log('Error at `unArchiService` after hit the endpoint.');
                console.log(response);
            });
    }

    alertEventInformation(message, type) {
        const alertPlaceholder = document.getElementById('liveAlertPlaceholder');
    
        const wrapper = document.createElement('div')
        wrapper.innerHTML = [
          `<div class="alert alert-${type} alert-dismissible" role="alert">`,
          `   <div>${message}</div>`,
          '   <button id="alertEventCloseButton" type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
          '</div>'
        ].join('')
      
        alertPlaceholder.append(wrapper);
    
        setTimeout(function() {
            document.getElementById("alertEventCloseButton").click();
        }, 5000);
    }

    /**
     * @returns {{inputArchiConcept: string}}|null}
     */
    formValidationError() {
        const error = {};

        if (['', null, undefined, 'Selecciona un elemento inicial'].includes(this.inputArchiConcept.value)) {
            error['inputArchiConcept'] = 'Campo obligatorio';
        }

        return (Object.keys(error).length === 0) ? null : error;
    }

     /**
     * @return {boolean}
     */
    formIsValid() {
        return this.formValidationError() === null;
    }

    updateViewToShowFormErrors() { 
        const errors = this.formValidationError();

        if (errors && errors.inputArchiConcept) {
            this.inputArchiConcept.classList.add('is-invalid');
            this.inputArchiConcept.classList.remove('is-valid');
            this.inputArchiConcept.nextElementSibling.textContent = errors.inputArchiConcept;

        }
    }

    updateViewToShowFormSuccess() {
        const errors = this.formValidationError();

        if (!errors?.inputArchiConcept) {
            this.inputArchiConcept.classList.remove('is-invalid');
            this.inputArchiConcept.classList.add('is-valid');
            this.inputArchiConcept.nextElementSibling.textContent = '';
        }
    }

    disableModalClose() {
        this.modal.dataset['bs.backdrop'] = 'static';
    }

    cleanInputArchiConceptStyle() {
        this.inputArchiConcept.classList.remove('is-invalid');
        this.inputArchiConcept.classList.remove('is-valid');
    }
}
