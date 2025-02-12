#from src.core.services.monitor import MonitorService

class FetchMetricsUseCase:
    def __init__(self, ssh_client):
        """
        :param ssh_client: Instance of SSHClient to handle SSH connections
        :param monitor_service: Instance of MonitorService to process metrics
        """
        self.ssh_client = ssh_client
        #self.monitor_service = monitor_service

    def execute(self, server):
        """
        Fetches metrics from a server via SSH
        :param server: Server instance containing connection details
        :return: Dict of fetched metrics
        """
        command = "df -h"
        print(server)
        try:
            print("Fetching metrics for server {}".format(server["ip_address"]))
            output = self.ssh_client.connect(server["ip_address"], server["port"], server["user"], command)
            #metrics = self.monitor_service.parse_metrics(output)
            return output
        except Exception as e:
            print("Error fetching metrics for server {}: {}".format(server["ip_address"], str(e)))
            return None
