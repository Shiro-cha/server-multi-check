import json


class MonitorService:
    def __init__(self, config,ssh_client):
        self.config = config
        self.ssh_client = ssh_client

    def start(self,command):
        
        servers = self.config.load_config("servers")["servers"]
        outputs = []
        for server in servers:
            output = self.ssh_client.connect(server["ip_address"], server["port"], server["user"], command)
            outputs.append(output)
        return outputs

    def restart(self):
        self.start()