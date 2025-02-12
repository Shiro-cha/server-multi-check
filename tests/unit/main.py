
from src.infrastructure.adapters.command.local_command import LocalCommand
from src.infrastructure.adapters.ssh_client.binary_ssh_connexion import BinarySSHConnexion
from src.core.use_cases.fetch_metrics import FetchMetricsUseCase

cmd = LocalCommand();

print("=======local command test=======")
print(cmd.execute("ls -l"))
print("=======ssh client test=======")

ssh = BinarySSHConnexion(cmd);
print(ssh.connect("192.168.10.201", 8442, "nomena30","df -h"))

print("=======metrics test =======")
fetch = FetchMetricsUseCase(ssh)
server=dict(ip_address="192.168.10.201", port=8442, user="nomena30", password="nomena30")
print(fetch.execute(server))
