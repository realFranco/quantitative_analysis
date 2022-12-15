# Backend Service

This folder will contain elements related to the backend service that will interact
using a REST service with the frontend.

## Environment Variables explanation

This project use some environment variables, make sure that you have read it before continue.

- `ARCHI_RUNNABLE`:
    - Description: Location of the Archi executable file, available only if you are
into a Linux distribution.

- `PROJECT_NAME`: 
    - Description: The name of the project by default will have the name `quantitative_analysis`, if the project 
    name change you should change this value as well.

- `PROJECT_LOCATION`: 
    - Description: Absolute route directory of the folder that contain this project.
    - Example: `/home/user/Documents/${PROJECT_NAME}/`

- `PROJECT_HTTP_PROTOCOL`:
    - Description: Protocol to communicate between the client and the server.
    - Example: `http`

- `PROJECT_LOCALHOST`:
    - Description: Local IP address stablish by the client in order to stablish a HTTP connection with the server.
    - Example: `127.0.0.1`

- `PROJECT_PORT`:
    - Description: Port number to use in conjunction with the IP address.
    - Example: `8000`

- `PROJECT_LOCALHOST_URL`:
    - Description: Base URL defined to stablish a HTTP connection between the client and server.

- `SCRIPT_CONFIG_LOCATION`:
    - Description: File where the jArchi scripts will collect configuration variables.
    For example, it will contain the location where to store the results from "Quantitative Analysis" algorithms.

- `COMPUTE_RESOURCE_LOCATION`:
    - Description: Relative route where the parser service will write a file. This file will be acting as "compute" inputs from the cloud provider into the "Quantitative Analysis" algorithm.

- `QUANTITATIVE_ANALYSIS_RESULT_LOCATION`: 
    - Description: Relative route used to expose the results from the "Quantitative Analysis" flow, and will be used to show to the user through the web service.

## Run this collection

The next button is a static link into a set of endpoints to observe the REST service.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/0068e6c6f67b77aecb9f?action=collection%2Fimport)

Create a Environment before run the collection and select it:

    - `baseUrl`: Backend host url, could be "http://127.0.0.1:8000" for example.

## Technology Stack

Technology stack used in order to develop the Front End service:

| Tool name | Tool version  | Reference                                                 | Used for |
|---        | ---           |---                                                        | ---      |
| python3   | v3.8.10       | [GitHub's cpython](https://github.com/python/cpython)     | Develop internal components and services. |
| FastAPI   | v0.85.0       | [GitHub's FastAPI](https://github.com/tiangolo/fastapi)   | Used as Back End framework, in order to develop a REST API. |
