

import json


class FetchMetricsUseCase:
    def __init__(self, ssh_client):
        """
        :param ssh_client: Instance of SSHClient to handle SSH connections
        """
        self.ssh_client = ssh_client

    def _execute(self, server, command):
        try:
            print("Fetching metrics for server {}".format(server["ip_address"]))
            output = self.ssh_client.connect(server["ip_address"], server["port"], server["user"], command)
            return self._to_json(output)
        except Exception as e:
            print("Error fetching metrics for server {}: {}".format(server["ip_address"], str(e)))
            return None

    def _to_json(self, myjson):
        try:
            return json.loads(myjson)
        except ValueError as e:
            print("Error parsing JSON: {}".format(str(e)))
            return None

    def get_disk_usage(self, server):
        command = "'python -' < src/ressource/scripts/monitor-disk.py"
        result = self._execute(server, command)
        return result[0] if result is not None else None

    def get_cpu_memory_usage(self, server):
        command = "'python -' < src/ressource/scripts/cpu-memory.py"
        result = self._execute(server, command)
        return result if result else None
