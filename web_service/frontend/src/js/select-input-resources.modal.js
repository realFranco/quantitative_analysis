export class SelectInputResourcesModal {
  /**
   * @type {HTMLDivElement}
   */
  modal = document.getElementById('selectInputResourcesModal');
  /**
   * @type {HTMLInputElement}
   */
  filesInput = document.getElementById(
    'selectInputResourcesModalInputResourcesFilesInput'
  );
  /**
   * @type {HTMLSelectElement}
   */
  cloudServiceProviderSelect = document.getElementById(
    'selectInputResourcesModalInputResourcesCloudServiceProviderSelect'
  );
  /**
   * @type {HTMLFormElement}
   */
  form = document.getElementById('selectInputResourcesModalForm');
  /**
   * @type {HTMLButtonElement}
   */
  cancelButton = document.getElementById(
    'selectInputResourcesModalCancelButton'
  );
  /**
   * @type {HTMLButtonElement}
   */
  uploadFilesButton = document.getElementById(
    'selectInputResourcesModalUploadFilesButton'
  );

  /**
   * @type {FilePond}
   */
  filePond = FilePond.create(this.filesInput);

  // apiUrl = 'localhost:PORT';
  apiUrl = 'http://127.0.0.1:8000';

  constructor() {
    this.initializeListeners();
  }

  initializeListeners() {
    this.uploadFilesButton.addEventListener('click', () => {
      this.disableModalClose();
      this.updateViewToShowFormSuccess();
      if (this.formIsInvalid()) {
        this.updateViewToShowFormErrors();
        return;
      }

      this.uploadFilesButton.setAttribute('disabled', 'true');
      const formData = new FormData();
      this.filePond
        .getFiles()
        .map((file) => file.file)
        .forEach((file) => formData.append('files', file, file.name));

      fetch(`${this.apiUrl}/parser/${this.cloudServiceProviderSelect.value}`, {
        method: 'POST',
        body: formData,
      })
        .then((response) => response.json())
        .then((response) => {
          // Files correctly uploaded.
          this.uploadFilesButton.removeAttribute('disabled');
          this.resetForm();
          if (true === response.parseResult) {
            // document append child | expose
            
            document.getElementById("selectInputResourcesModalCloseButton").click();

            this.alertEventInformation('¡Elementos de entrada analizados correctamente!', 'success');
          }
        })
        .catch((response) => {
          this.uploadFilesButton.removeAttribute('disabled');
          console.log({ response });

          // document append child | expose
          document.getElementById("selectInputResourcesModalCloseButton").click();
          
          this.alertEventInformation('Sucedió un problema al analizar datos de entrada!', 'warning');
        });
    });
  }

  /**
   *
   * @returns {{cloudServiceProvider?: string, filesInput?: string}|null}
   */
  formValidationErrors() {
    const errors = {};
    if (['', null, undefined].includes(this.cloudServiceProviderSelect.value)) {
      errors['cloudServiceProvider'] = 'Campo obligatorio';
    }

    if (this.filePond.status === 0) {
      errors['filesInput'] = 'Campo obligatorio';
    }

    if (Object.keys(errors).length === 0) {
      return null;
    }
    return errors;
  }

  /**
   * @return {boolean}
   */
  formIsValid() {
    return this.formValidationErrors() === null;
  }

  /**
   * @return {boolean}
   */
  formIsInvalid() {
    return !this.formIsValid();
  }

  updateViewToShowFormErrors() {
    const errors = this.formValidationErrors();
    if (errors.cloudServiceProvider) {
      this.cloudServiceProviderSelect.classList.add('is-invalid');
      this.cloudServiceProviderSelect.classList.remove('is-valid');
      this.cloudServiceProviderSelect.nextElementSibling.textContent =
        errors.cloudServiceProvider;
    }
    if (errors.filesInput) {
      this.filePond.element.classList.add('is-invalid');
      this.filePond.element.classList.remove('is-valid');
      this.filePond.element.nextElementSibling.textContent = errors.filesInput;
    }
  }

  updateViewToShowFormSuccess() {
    const errors = this.formValidationErrors();
    if (!errors?.cloudServiceProvider) {
      this.cloudServiceProviderSelect.classList.remove('is-invalid');
      this.cloudServiceProviderSelect.classList.add('is-valid');
      this.cloudServiceProviderSelect.nextElementSibling.textContent = '';
    }
    if (!errors?.filesInput) {
      this.filePond.element.classList.remove('is-invalid');
      this.filePond.element.classList.add('is-valid');
      this.filePond.element.nextElementSibling.textContent = '';
    }
  }

  resetForm() {
    [this.cloudServiceProviderSelect, this.filePond.element].forEach(
      (element) => {
        element.classList.remove('is-valid', 'is-invalid');
        element.nextElementSibling.textContent = '';
      }
    );
    this.filePond.removeFiles();
    this.cloudServiceProviderSelect.options[0].selected = true;
  }

  disableModalClose() {
    this.modal.dataset['bs.backdrop'] = 'static';
  }

  enableModalClose() {}

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
}
