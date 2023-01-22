import platform
import os

from src.models.ServiceStatus import ServiceStatus
from src.utils.ArchiStatus import ArchiStatus


class ArchiRunner:

    @staticmethod
    def run_service() -> ServiceStatus:
        """
        This method will help execute an internal command that will run the "Archi" application.
        """
        try:
            if None == os.getenv('ARCHI_RUNNABLE'):
                return ServiceStatus(
                    info='Environment variable `ARCHI_RUNNABLE` is not set.',
                    isArchiRunning=False
                )

            if True == ArchiStatus.check_service().isArchiRunning:
                return ServiceStatus(
                    info='"Archi" service is already running.',
                    isArchiRunning=True
                )

            # Check the output of the process to control the response
            if platform.system() == 'Darwin':
                os.popen(f'cd / && .{os.getenv("ARCHI_RUNNABLE")}')
            else:  # Check how it's look on Ubuntu.
                os.popen(f'sh {os.getenv("ARCHI_RUNNABLE")}')

            return ServiceStatus(
                info='"Archi" service it is running now.',
                isArchiRunning=True
            )

        except Exception as error:
            print(f'At `ArchiRunner.run_service` method: {error}')

            return ServiceStatus(
                info='Unable to run the "Archi" service.',
                isArchiRunning=False
            )
