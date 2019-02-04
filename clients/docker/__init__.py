"""Docker client module."""

import subprocess

import docker

from .containers import DockerContainerMixin
from .networks import DockerNetworksMixin
from .images import DockerImagesMixin


class DockerClient(DockerContainerMixin, DockerNetworksMixin, DockerImagesMixin):

    """Special client for docker commands."""

    def __init__(self):
        self.client = docker.from_env()

    def call(self, command):
        """Call method to execute shell commands."""
        return subprocess.check_output(command).decode()
