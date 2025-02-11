from src.infrastructure.adapters.command.command_interface import CommandeInterface
import subprocess


class LocalCommand(CommandeInterface):
    def execute(self, command):
        if not command:
            raise ValueError("command cannot be null or empty")

        try:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout, stderr = process.communicate()
            if stderr:
                print("Error executing command: {}".format(stderr.decode('utf-8')))
            return stdout.decode('utf-8')
        except subprocess.CalledProcessError as e:
            if hasattr(e, 'output') and e.output:
                print("Error executing command: {}".format(e.output.decode('utf-8')))
            raise
