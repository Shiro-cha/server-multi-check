import json
from src.core.services.identity import IdentityService
from src.core.services.monitor import MonitorService
from src.core.use_cases.install_identity import InstallIdentityUseCase
from src.infrastructure.adapters.command.local_command import LocalCommand
from src.infrastructure.adapters.ssh_client.binary_ssh_connexion import BinarySSHConnexion
from src.core.use_cases.fetch_metrics import FetchMetricsUseCase
from src.infrastructure.config_loader import ConfigLoader

cmd = LocalCommand();

#print("=======local command test=======")
#print(cmd.execute("ls -l"))
#print("=======ssh client test=======")

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

identity_service = IdentityService(config)
use_case = InstallIdentityUseCase(identity_service)

use_case.execute()


monitorservice = MonitorService(config,ssh)
#command = "'python -' < src/ressource/scripts/monitor-disk.py"
#monitorservice.start(command)
#for output in monitorservice.start(command):
#    print(output)

fetch = FetchMetricsUseCase(monitorservice)
print("=======disk usage=======")
disk_usage = fetch.get_disk_usage()
# convert the json string to a python dictionary
if disk_usage:
    disk_usage_dict = json.loads(disk_usage)
    for disk in disk_usage_dict:
        print(disk)
        print(f"MountPoint: {disk['MountPoint']}")
        print(f"  Total: {round(disk['Total'], 1)} GB")
        print(f"  Used: {round(disk['Used'], 1)} GB")
        print(f"  Free: {round(disk['Free'], 1)} GB")
        print(f"  Available: {round(disk['Available'], 1)} GB")
        print("-" * 40)

#print("=======cpu memory usage=======")
#print(fetch.get_cpu_memory_usage())
