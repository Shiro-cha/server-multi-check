


from src.infrastructure.adapters.ssh_client.ssh_client_interface import SSHClientInterface

class BinarySSHConnexion(SSHClientInterface):
    def __init__(self, command_executor):
        self.command_executor = command_executor

    def _create_ssh_command(self, host, port, user, command=None, host_key=None,key=None,timeout=None):
        """
        Creates the ssh command as a list of strings.
        :return: The ssh command as a list of strings.
        """
        command_parts = ['ssh']
        if key is not None:
            command_parts.extend(['-i', key])

        
        if port is not None:
            command_parts.extend(['-p', str(port)])
        if host_key is not None:
            command_parts.extend(['-o', 'HostKeyAlgorithms={}'.format(host_key)])

        if timeout is not None:
            command_parts.extend(['-o', 'ConnectTimeout={}'.format(timeout)])

        user_host = "{}@{}".format(user, host)
        command_parts.append(user_host)

        if command:
            command_parts.append(command)

        return command_parts

    def connect(self, host, port, user, command=None, password=None, key=None,host_key=None, key_passphrase=None, timeout=None):
        ssh_command = self._create_ssh_command(host, port, user, command, host_key,key,timeout)
        ssh_command_str = ' '.join(ssh_command)

        if password:
            print("Direct password authentication is not supported. Please use key authentication.")
        if key_passphrase is not None:
            print("Key passphrase is not supported. Please use an unencrypted key.")


        return self.command_executor.execute(ssh_command_str)

    def close(self):
        """Closes any ongoing connections. Currently a no-op as connections are not persistent."""
        pass
