"""
The Archi application requires to import another elements, the constant `RAW_PROJECT_LOCATION` expose
the absolute route location stablish for the project.

This file will edit the main jArchi script exposed.

Execution flow:

> cd web_service/backend
> source venv/bin/activate && python3 src/tuning.py

or

> make tuning
"""
import os

from dotenv import load_dotenv


MAIN_JARCHI_SCRIPT_LOCATION: str = '../../scripts/script.ajs'

def setProjectLocation() -> None:

    with open(MAIN_JARCHI_SCRIPT_LOCATION, 'r') as file:
        oldScript = file.read()
        newScript = oldScript.replace('_PROJECT_LOCATION_', os.getenv('PROJECT_LOCATION'))
        file.close()

    if oldScript == newScript:
        print('No editions applied during tunning process.')
        return

    with open(MAIN_JARCHI_SCRIPT_LOCATION, 'w') as file:
        file.write(newScript)
        file.close()

    print('Editions applied during tunning process.')

    return

if __name__ == '__main__':
    load_dotenv()
    setProjectLocation()
