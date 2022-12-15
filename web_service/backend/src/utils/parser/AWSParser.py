import os
import json
from typing import Dict, List

from fastapi import UploadFile

from src.models.ParserStatus import ParserStatus
from src.models.AWSLogTrace import ContainerLogTrace, LogTrace


class AWSParser:

    @staticmethod
    def collect_compute_resources() -> ParserStatus:
        """Temporal method. Copy read the content from an example file related with
        services and compute resources. After implement the static method `AWSParser.read()`
        this method will be removed.
        """
        data = ParserStatus(data={}, info='No data collected.')

        with open('../../' + os.getenv('COMPUTE_RESOURCE_LOCATION'), 'r') as f:
            data.data = json.loads(f.read())
            data.info = 'Data collected.'
            f.close()

        return data

    @staticmethod
    def parse_performance_logs(containerLogTrace: ContainerLogTrace, trace: Dict):
        for internalTrace in trace:
            # print(internalTrace['@message'])
            # print(f'log trace: {logTrace}')
            containerLogTrace.parse(
                LogTrace(
                    requestId=internalTrace['request_id'],
                    metrics=internalTrace['@message'],
                )
            )

        return containerLogTrace

    @staticmethod
    def parse_status_code_logs(containerLogTrace: ContainerLogTrace, trace: Dict):
        for internalTrace in trace:
            logTrace = LogTrace(
                requestId=internalTrace['@requestId'],
                code=internalTrace['code'],
            )
            containerLogTrace.parse(logTrace)

        return containerLogTrace

    @staticmethod
    def parse_logs(timeWindowRange: int, data: List[UploadFile], location: str = None) -> bool:
        """
        Read two logs from AWS context, make a group by time window and write a result object.

        timeWindowRange: int. Useful for group the logs. This argument represent "seconds"
        in order to group.

        data: List[str]. Will be the file objects to be parsed
        More info about `UploadFile` class: https://fastapi.tiangolo.com/tutorial/request-files/#uploadfile

        location: str. Location where the resource object file will be stored. By default it is
        the environment variable `COMPUTE_RESOURCE_LOCATION`.
        """
        location = '../../' + os.getenv('COMPUTE_RESOURCE_LOCATION') if None == location else location
        
        containerLogTrace = ContainerLogTrace(data=[])

        for inputLogFile in data:
            logTraceContent = inputLogFile.file.read()
            logTraceContent = logTraceContent.decode('utf-8')

            trace = json.loads(logTraceContent)
            if 'performanceLogInsight.json' in inputLogFile.filename:
                containerLogTrace = AWSParser.parse_performance_logs(containerLogTrace, trace)

            elif 'statusCode.json' in inputLogFile.filename:
                containerLogTrace = AWSParser.parse_status_code_logs(containerLogTrace, trace)

            else:
                print(f'The filename "{inputLogFile.filename}" it is an incorrect AWS Log file.')

        containerLogTrace.clean()

        # Make use of the List object returned here and store if for jArchi scripts.
        logGroup = containerLogTrace.groupByTimeWindow(timeWindowRange=timeWindowRange)
        # print(f'log groups returned: {len(logGroup)}\n')

        with open(location, 'w') as f:
            f.write(json.dumps( [log.dict() for log in logGroup] ))
            f.close()

        return True
