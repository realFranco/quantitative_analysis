# Renombrar archivo a AWSLogTrace
# AWSInvokeStatus

from typing import Dict, List
from pydantic import BaseModel
from src.models.TimeWindow import TimeWindow, CapMetric

# Estas clases contendrán lógica de negocio y "solo" para el contexto AWS.


class LogTrace(BaseModel):
    requestId: str = None
    code: str = None
    metrics: Dict = None

    def parse(self, requestId: str = None, metrics: Dict = None, code: str = None ):
        self.requestId = requestId if requestId != None else self.requestId
        self.metrics = metrics if metrics != None else self.metrics
        self.code = code if code != None else self.code

        return None
    

class ContainerLogTrace(BaseModel):
    data: List[LogTrace] = None
    
    def _isRequestIdExist(self, requestId) -> bool:
        if not self.data:
            return False

        for trace in self.data:
            if requestId == trace.requestId:
                return True

        return False

    def parse(self, logTrace: LogTrace):
        # print(f'parse log trace: {logTrace}')
        if logTrace.requestId == None:
            return None

        if self._isRequestIdExist(logTrace.requestId) == False:
            self.data.append(logTrace)

            return None

        for trace in self.data:
            if trace.requestId == logTrace.requestId:
                # print('match found!')
                # print(f'before parse: {logTrace}\n')
                # print(logTrace.metrics)
                trace.parse(logTrace.requestId, logTrace.metrics, logTrace.code)
                # print(f'after parse: {logTrace}\n\n')

                return None

    def groupByTimeWindow(self, timeWindowRange: int = 15) -> List[TimeWindow]:
        """
        Agrupará logs tras la separación en la ventana de tiempo, la ventana de 
        tiempo dependerá del parámetro `timeWindowRange`. 
        
        Aplicará conversión para cómputo observar las métricas de cómputo.

        El objeto a retornar deberá ser similar a los que están dentro del archivo `jArchiComputeResources.json`.

        :param timeWindowRange int. Tamaño de la venta de tiempo, expresado en segundos.
        """
        # print(f'Cantidad de logs a agrupar: {len(self.data)}')

        if 0 == len(self.data):
            return []

        logTrace = self.data[0]
        i, n = 1, len(self.data)
        currentTimeWindow = 0

        # Add the first element in the first time window checking if correctly ends or not
        # Cast the flat into 2 digits
        service = CapMetric(
            name=logTrace.metrics['function_name'],
            resources={
                'timestamp': int(logTrace.metrics['_aws']['Timestamp']),
                'cpu': round(logTrace.metrics['cpu_user_time'] / logTrace.metrics['cpu_total_time'], 2),
                'ram': round(logTrace.metrics['memory_utilization'] / 100, 2),
                'network': round(logTrace.metrics['tx_bytes'] / logTrace.metrics['total_network'], 2),
                'storage': round(logTrace.metrics['tmp_used'] / logTrace.metrics['tmp_max'], 2)
            }
        )
        timeWindow = TimeWindow(
            timeWindow=currentTimeWindow,
            serviceEnds=[service] if logTrace.code == None or logTrace.code == '' else [],
            serviceNotEnds=[service] if not (logTrace.code == None or logTrace.code == '') else []
        )
        groups = [timeWindow]

        while i < n:
            # Share the same group.
            while i < n and self.data[i].metrics['_aws']['Timestamp'] - logTrace.metrics['_aws']['Timestamp'] <= timeWindowRange:
                # Services share the same time window
                service = CapMetric(
                    name=self.data[i].metrics['function_name'],
                    resources={
                        'timestamp': int(self.data[i].metrics['_aws']['Timestamp']),
                        'cpu': round(self.data[i].metrics['cpu_user_time'] / self.data[i].metrics['cpu_total_time'], 2),
                        'ram': round(self.data[i].metrics['memory_utilization'] / 100, 2),
                        'network': round(self.data[i].metrics['tx_bytes'] / self.data[i].metrics['total_network'], 2),
                        'storage': round(self.data[i].metrics['tmp_used'] / self.data[i].metrics['tmp_max'], 2)
                    }
                )
                if logTrace.code == None or logTrace.code == '':
                    # Job ends "ok" -> servicesEnds
                    timeWindow.serviceEnds.append(service)
                else:
                    # Job ends "not ok" -> serviceNotEnds
                    timeWindow.serviceNotEnds.append(service)

                i += 1

            # Internal while and external while must share the same indexing condition.
            if i == n:
                break

            # New group, create one for the current log.
            currentTimeWindow += 1
            service = CapMetric(
                name=self.data[i].metrics['function_name'],
                resources={
                    'timestamp': self.data[i].metrics['_aws']['Timestamp'],
                    'cpu': round(self.data[i].metrics['cpu_user_time'] / self.data[i].metrics['cpu_total_time'], 2),
                    'ram': round(self.data[i].metrics['memory_utilization'] / 100, 2),
                    'network': round(self.data[i].metrics['tx_bytes'] / self.data[i].metrics['total_network'], 2),
                    'storage': round(self.data[i].metrics['tmp_used'] / self.data[i].metrics['tmp_max'], 2)
                }
            )
            logTrace = self.data[i]
            i += 1
            timeWindow = TimeWindow(
                timeWindow=currentTimeWindow,
                serviceEnds=[service] if logTrace.code == None or logTrace.code == '' else [],
                serviceNotEnds=[service] if not (logTrace.code == None or logTrace.code == '') else []
            )
            groups.append(timeWindow)

        return groups

    @staticmethod
    def _isValidTrace(self) -> bool:
        return self.requestId != None and self.code != None and self.metrics != None

    def clean(self):
        """Due the high amount of logs that could be collect during the ingestion or parsing flows,
        there exists some log trace not required, this method will remove them."""
        if self.data == None:
            return None

        self.data = [trace for trace in self.data if ContainerLogTrace._isValidTrace(trace) == True]

        return None
