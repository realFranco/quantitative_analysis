import os
import re

from src.models.ServiceStatus import ServiceStatus
from src.config.Commands import Commands


class ArchiStatus:

    @staticmethod
    def check_service() -> ServiceStatus:
        try:
            java_pid = os.popen(Commands.LINUX_JAVA_PROCESS_ID).read()
            if not java_pid:
                return ServiceStatus(
                    info='No "java" process instantiated.',
                    isArchiRunning=False
                )

            java_pid_number = re.findall(r'\d+', java_pid)
            if 0 == len(java_pid_number):
                return ServiceStatus(
                    info='No "java PID" collected.',
                    isArchiRunning=False
                )

            for pid in java_pid_number:
                process_executable = os.popen(Commands.LINUX_PROCESS_ID_PATH.format(pid=pid)).read()
                if len(process_executable) > 0:
                    return ServiceStatus(
                        info='Archi is already running on host!',
                        isArchiRunning=True
                    )

            return ServiceStatus(
                info='Archi is not running on host.',
                isArchiRunning=False
            )

        except Exception as error:
            print(f'At class `ArchiStatus` and `check_service` method: {error} ')

            return ServiceStatus(
                info='Archi is not running on host.',
                isArchiRunning=False
            )
