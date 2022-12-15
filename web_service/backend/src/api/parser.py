"""
Parse router.
"""
import traceback

from fastapi import APIRouter
from fastapi import UploadFile
from typing import List

from src.config.Routes import Routes
from src.config.Tags import Tags
from src.config.Messages import Messages
from src.utils.parser.AWSParser import AWSParser
from src.models.CloudService import CloudService


parser = APIRouter(
    prefix=Routes.PARSER,
    tags=[Tags.parser],
    responses={404: Messages.NOT_FOUND}
)

@parser.post('/{cloud_service}')
async def parse_aws(cloud_service: str, files: List[UploadFile], timeWindowRange: int = 15):
    """Return an object to expose the resources into the front end diagram."""
    try:
        valid_cloud_services = [service.value for service in CloudService]
        if cloud_service not in valid_cloud_services:
            return {
                'message': f'The current cloud service "{cloud_service}" is not inside the valid Cloud Services. ' + \
                    f'Correct values are {", ".join(valid_cloud_services)}'
            }

        if 0 == len(files):
            return {
            'message': 'Please upload files into the parser service.',
            'parseResult': False
        }

        return {
            'message': 'Logs parsed.',
            'parseResult': AWSParser.parse_logs(
                timeWindowRange=timeWindowRange,
                data=files,
                location=None,
            )
        }

    except Exception as error:
        print('At route "archi" and `parse_aws` endpoint ', error)
        traceback.print_exc()

        return {
            'errorMessage': str(error)
        }
