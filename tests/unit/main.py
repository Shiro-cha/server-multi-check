
from src.core.services.monitor import MonitorService
from src.infrastructure.adapters.command.local_command import LocalCommand
from src.infrastructure.adapters.ssh_client.binary_ssh_connexion import BinarySSHConnexion
from src.core.use_cases.fetch_metrics import FetchMetricsUseCase
from src.infrastructure.config_loader import ConfigLoader

cmd = LocalCommand();

print("=======local command test=======")
print(cmd.execute("ls -l"))
print("=======ssh client test=======")

ssh = BinarySSHConnexion(cmd);
#print(ssh.connect("192.168.10.201", 8442, "nomena30","df -h"))
#
#print("=======metrics test =======")

#server=dict(ip_address="192.168.10.201", port=8442, user="nomena30", password="nomena30")
#print("=======disk usage=======")
#print(fetch.get_disk_usage(server))
#print("=======cpu memory usage=======")
#print(fetch.get_cpu_memory_usage(server))


print("=======laod config test=======")
config= ConfigLoader("config")
print(config.load_config("servers"))

monitorservice = MonitorService(config,ssh)
#command = "'python -' < src/ressource/scripts/monitor-disk.py"
#monitorservice.start(command)
#for output in monitorservice.start(command):
#    print(output)

fetch = FetchMetricsUseCase(monitorservice)
print("=======disk usage=======")
print(fetch.get_disk_usage())

print("=======cpu memory usage=======")
print(fetch.get_cpu_memory_usage())
