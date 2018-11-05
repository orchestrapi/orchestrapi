"""Clients module."""
import subprocess


class ShellClient:

    """Base client.
        For base shell operations."""

    @staticmethod
    def call(command):
        """Call method to execute shell commands."""
        return subprocess.check_output(command).decode()
