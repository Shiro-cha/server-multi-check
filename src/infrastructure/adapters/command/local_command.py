from src.infrastructure.adapters.command.command_interface import CommandeInterface
import subprocess


class LocalCommand(CommandeInterface):

    def _validate_command(self, command):
        if not command:
            raise ValueError("Command cannot be null or empty")

    def _check_error(self, stderr):
        if stderr:
            print("Error executing command: {}".format(stderr))

    def _check_output_error(self, stdout):
        if not stdout:
            print("Error: No output from command execution")
    def _convert_to_string(self, stdout):
        return stdout.decode("utf-8")

    def execute(self, command):
        self._validate_command(command)
        print("Executing command: {}".format(command))
        try:
            process = subprocess.Popen(
                command, shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            self._check_error(stderr)
            self._check_output_error(stdout)
            
            return self._convert_to_string(stdout)
        except subprocess.CalledProcessError as e:
            print("Error executing command: {}".format(getattr(e, 'output', 'Unknown error')))
            raise
