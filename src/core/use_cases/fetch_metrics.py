#from src.core.services.monitor import MonitorService

import json


class FetchMetricsUseCase:
    def __init__(self, ssh_client):
        """
        :param ssh_client: Instance of SSHClient to handle SSH connections
        :param monitor_service: Instance of MonitorService to process metrics
        """
        self.ssh_client = ssh_client
        #self.monitor_service = monitor_service

    def _execute(self, server,command):
        
        try:
            print("Fetching metrics for server {}".format(server["ip_address"]))
            output = self.ssh_client.connect(server["ip_address"], server["port"], server["user"], command)
            print("to json")
            return self._to_json(output)
        except Exception as e:
            print("Error fetching metrics for server {}: {}".format(server["ip_address"], str(e)))
            return output
    def _to_json(self, myjson):
        try:
            return json.loads(myjson)
            
        except ValueError as e:
            print("Error parsing JSON: {}".format(str(e)))
            return myjson
        
    def get_disk_usage(self,server):
        command = "'python -' < src/ressource/scripts/monitor-disk.py"
        return self._execute(server,command)[0]

    def get_cpu_memory_usage(self,server):
        command = "'python -' < src/ressource/scripts/cpu-memory.py"
        return self._execute(server,command)["cpu_usage"]