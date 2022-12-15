"""
Example of execution.

cd web_service/backend

python3 -m pytest test/

python3 -m pytest test/ -vs
"""
import json

from src.models.AWSLogTrace import ContainerLogTrace, LogTrace


def collect_logs_group(timeWindowRange: int = 15):
    """Helper function, given a json file, with jobs, return an list of `TimeWindow`.
    """
    containerLogTrace = ContainerLogTrace()
    containerLogTrace.data = []
    generatedLogLocation = 'test/utils/parser/logsGenerated15SecGap.json'

    with open(generatedLogLocation, 'r') as f:
        for log in json.loads(f.read()):
            containerLogTrace.data.append(LogTrace(**log))
        f.close()

    return containerLogTrace.groupByTimeWindow(timeWindowRange=timeWindowRange)

def test_compute_metrics_groups_15_secs_grouping():
    assert len(collect_logs_group(timeWindowRange=15)) == 6

def test_compute_metrics_groups_50_secs_grouping():
    assert len(collect_logs_group(timeWindowRange=50)) == 3

def test_compute_metrics_groups_90_secs_grouping():
    assert len(collect_logs_group(timeWindowRange=90)) == 2

def test_compute_metrics_groups_135_secs_grouping():
    assert len(collect_logs_group(timeWindowRange=135)) == 1
