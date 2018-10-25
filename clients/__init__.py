import subprocess

class ShellClient:

    @staticmethod
    def call(command):
        return subprocess.check_output(command).decode()
