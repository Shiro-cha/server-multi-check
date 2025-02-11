from src.infrastructure.adapters.ssh_client.ssh_client_interface import SSHClientInterface

class BinarySSHConnexion(SSHClientInterface):
    def __init__(self, command_executor):
        self.command_executor = command_executor

    def _add_key_option(self, command_parts, key):
        if key is not None:
            command_parts.extend(['-i', key])

    def _add_port_option(self, command_parts, port):
        if port is not None:
            command_parts.extend(['-p', str(port)])

    def _add_host_key_option(self, command_parts, host_key):
        if host_key is not None:
            command_parts.extend(['-o', 'HostKeyAlgorithms={}'.format(host_key)])

    def _add_timeout_option(self, command_parts, timeout):
        if timeout is not None:
            command_parts.extend(['-o', 'ConnectTimeout={}'.format(timeout)])

    def _add_user_host(self, command_parts, user, host):
        user_host = "{}@{}".format(user, host)
        command_parts.append(user_host)

    def _add_remote_command(self, command_parts, command):
        if command:
            command_parts.append(command)

    def _create_ssh_command(self, host, port, user, command=None, host_key=None, key=None, timeout=None):
        command_parts = ['ssh']
        self._add_key_option(command_parts, key)
        self._add_port_option(command_parts, port)
        self._add_host_key_option(command_parts, host_key)
        self._add_timeout_option(command_parts, timeout)
        self._add_user_host(command_parts, user, host)
        self._add_remote_command(command_parts, command)
        return command_parts

    def _validate_auth_parameters(self, password, key_passphrase):
        if password:
            print("Direct password authentication is not supported. Please use key authentication.")
        if key_passphrase is not None:
            print("Key passphrase is not supported. Please use an unencrypted key.")

    def connect(self, host, port, user, command=None, password=None, key=None, host_key=None, key_passphrase=None, timeout=None):
        self._validate_auth_parameters(password, key_passphrase)
        ssh_command = self._create_ssh_command(
            host=host,
            port=port,
            user=user,
            command=command,
            host_key=host_key,
            key=key,
            timeout=timeout
        )
        ssh_command_str = ' '.join(ssh_command)
        return self.command_executor.execute(ssh_command_str)

    def close(self):
        """Closes any ongoing connections. Currently a no-op as connections are not persistent."""
        pass