from src.core.services.monitor import MonitorService
from src.infrastructure.adapters.ssh_client import SSHClient

class FetchMetricsUseCase:
    def __init__(self, ssh_client, monitor_service):
        """
        :param ssh_client: Instance of SSHClient to handle SSH connections
        :param monitor_service: Instance of MonitorService to process metrics
        """
        self.ssh_client = ssh_client
        self.monitor_service = monitor_service

    def execute(self, server):
        """
        Fetches metrics from a server via SSH
        :param server: Server instance containing connection details
        :return: Dict of fetched metrics
        """
        command = "cat /proc/meminfo && cat /proc/stat && df -h"
        
        try:
            output = self.ssh_client.execute_command(server, command)
            #metrics = self.monitor_service.parse_metrics(output)
            return output
        except Exception as e:
            print("Error fetching metrics for server {}: {}".format(server.host, str(e)))
            return None
