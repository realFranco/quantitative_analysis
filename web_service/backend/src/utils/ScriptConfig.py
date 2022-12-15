import os
import json


class ScriptConfig():

    @staticmethod
    def export_configurations() -> None:
        with open('../../' + os.getenv('SCRIPT_CONFIG_LOCATION'), 'w') as f:
            f.write(json.dumps(
                    {   
                        'ARCHI_RUNNABLE': os.getenv('ARCHI_RUNNABLE'),
                        'PROJECT_LOCATION': os.getenv('PROJECT_LOCATION'),
                        'COMPUTE_RESOURCE_LOCATION': os.getenv('COMPUTE_RESOURCE_LOCATION'),
                        'QUANTITATIVE_ANALYSIS_RESULT_LOCATION': os.getenv('QUANTITATIVE_ANALYSIS_RESULT_LOCATION'),
                    }
                ))
            f.close()

    @staticmethod
    def set_property(key: str, value: str) -> None:
        configuration_object = {}
        with open('../../' + os.getenv('SCRIPT_CONFIG_LOCATION'), 'r') as f:
            configuration_object = json.loads(f.read())
            f.close()
        
        if configuration_object != {}:
            configuration_object.update({key: value})
            # print(f'configuration object: {configuration_object}')
            with open('../../' + os.getenv('SCRIPT_CONFIG_LOCATION'), 'w') as f:
                f.write(json.dumps(configuration_object))
                f.close()
