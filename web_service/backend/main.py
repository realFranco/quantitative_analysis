"""
Execution example.

> cd web_service/backend
> source venv/bin/activate && uvicorn main:app --reload

Frontend: http://127.0.0.1:8000/src/index.html

Backend: http://127.0.0.1:8000/docs | http://127.0.0.1:8000/redoc
"""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import uvicorn

from src.api.archi import archi
from src.api.parser import parser
from src.api.result import result
from src.utils.ScriptConfig import ScriptConfig
from src.config.Tags import Tags


STATIC_RESULT_FILE_LOCATION = 'resources/archi.elements.json'
load_dotenv()  # Take environment variables from .env.
app = FastAPI()

# Include the rest of the routers
app.include_router(archi)
app.include_router(parser)
app.include_router(result)

ScriptConfig.export_configurations()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/src', StaticFiles(directory='../frontend/src'), name='src')

@app.get('/', tags=[Tags.redirection])
async def redirection() -> None:
    return RedirectResponse(url=f'{os.getenv("PROJECT_LOCALHOST_URL")}/src/index.html')

if __name__ == '__main__':
    uvicorn.run(app, host=str(os.getenv("PROJECT_LOCALHOST")), port=int(os.getenv("PROJECT_PORT")))
