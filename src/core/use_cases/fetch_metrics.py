

import json


class FetchMetricsUseCase:
    def __init__(self, monitor_service):
        """
        :param ssh_client: Instance of SSHClient to handle SSH connections
        """
        self.monitor_service = monitor_service

    def _execute(self, command):
        try:
            output = self.monitor_service.start(command)
            
            return self._to_json(json.dumps(output))
        except Exception as e:
            return None

    def _to_json(self, myjson):
        try:
            return json.loads(myjson)
        except ValueError as e:
            print("Error parsing JSON: {}".format(str(e)))
            return None

    def get_disk_usage(self):
        command = "'python -' < src/ressource/scripts/monitor-disk.py"
        result = self._execute( command)
        return result[0] if result is not None else None

    def get_cpu_memory_usage(self):
        command = "'python -' < src/ressource/scripts/cpu-memory.py"
        result = self._execute(command)
        return result if result else None
