
from src.infrastructure.adapters.command.local_command import LocalCommand
from src.infrastructure.adapters.ssh_client.binary_ssh_connexion import BinarySSHConnexion

cmd = LocalCommand();

print("=======local command test=======")
print(cmd.execute("ls -l"))
print("=======ssh client test=======")

ssh = BinarySSHConnexion(cmd);
print(ssh.connect("192.168.10.201", 8442, "nomena30","df -h"))