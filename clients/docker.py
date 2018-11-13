"""Docker client module."""
import json

from django.conf import settings

from . import ShellClient
from .git import GitClient as gclient
from .helpers import Container


class DockerClient(ShellClient):

    """Special client for docker commands."""

    @staticmethod
    def ps():
        """Shows all running commands using 'docker ps' command."""
        docker_ps_template = [
            "docker", "ps",
            "--format", '"{{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}"']
        result = DockerClient.call(docker_ps_template)
        result = [
            r.replace('"', '').split(
                '\t') for r in result.split('\n') if r != '']
        return [Container(*r) for r in result]

    @staticmethod
    def container_status(container_id):
        """Returns status of a given container by id."""
        running_containers = DockerClient.ps()
        for container in running_containers:
            if container.id == container_id:
                return container.status
        return None

    @staticmethod
    def container_id(container_name):
        """Returns containers ID given the name."""
        running_containers = DockerClient.ps()
        for container in running_containers:
            if container.name == container_name:
                return container.id
        return None

    @staticmethod
    def _start(container_model):
        """Start command given the container name."""
        template = ['docker', 'start', container_model.name]
        return DockerClient.call(template).replace('\n', '')

    @staticmethod
    def build(app):
        """Builds a container. DEPRECATED"""
        template = [
            'docker', 'build', '-t',
            f'local/{app.slug}',
            f'{settings.GIT_PROJECTS_ROUTE}/{app.git.get("name")}/.']
        return DockerClient.call(template)

    @staticmethod
    def build_from_image_model(image, git_name):
        """Builds a container using an Image instance."""
        gclient.checkout_tag(git_name, image.tag)
        template = [
            'docker', 'build', '-t',
            f'{image.image_tag}',
            f'{settings.GIT_PROJECTS_ROUTE}/{git_name}/.']
        return DockerClient.call(template)

    @staticmethod
    def pull_from_dockerhub(image_name):
        """Pulls an image from docker hub."""
        template = [
            'docker', 'pull', f'{image_name}']
        return DockerClient.call(template)

    @staticmethod
    def image_id(image_name):
        """Returns an image id given its name."""
        template = ['docker', 'images', image_name, '-q']
        return DockerClient.call(template).replace('\n', '')

    @staticmethod
    def image_id_and_size(image_name):
        """Returns a tuble with image id and size, given the image name."""
        template = ['docker', 'images', image_name,
                    '--format', '"{{.ID}}\t{{.Size}}"']
        return DockerClient.call(template).replace('\n', '').replace('"', '').split('\t')

    @staticmethod
    def _stop(container_model):
        """Stops a container given its model."""
        template = ['docker', 'stop', container_model.name]
        return DockerClient.call(template).replace('\n', '')

    @staticmethod
    def remove(container_model):
        """Removes a container."""
        template = ['docker', 'rm', '-f', container_model.name]
        DockerClient.call(template)

    @staticmethod
    def remove_image(image_model):
        """Removes an image."""
        template = ['docker', 'rmi', '-f', image_model.image_tag]
        DockerClient.call(template)

    @staticmethod
    def docker_start(container_model, instance_name=None):
        """Starts a container with 'start' command if it exists, 'run' it if not."""
        if container_model.container_id:
            DockerClient._start(container_model)
        else:
            DockerClient._run(container_model, instance_name=instance_name)

    @staticmethod
    def inspect(container_model):
        """Returns container meta data."""
        template = ['docker', 'inspect', container_model.name]
        response = DockerClient.call(template)
        return json.loads(response)[0]

    @staticmethod
    def _run(container_model, instance_name=None):
        """Runs a container using 'run' command."""
        template = ["docker", "run"]
        if container_model.params != {}:
            for param in container_model.params.keys():
                if param == 'e':
                    for par_e, par_e_val in container_model.params['e'].items():
                        template.append(f'-{param}')
                        template.append(f'{par_e}={par_e_val}')
                elif param == 'v':
                    for volumen in container_model.params['v']:
                        template.append(f'-{param}')
                        template.append(volumen)
                else:
                    template.append(f'-{param}')
                    template.append(container_model.params[param])
        template.append('--name')
        template.append(instance_name or container_model.name)
        template.append('-d')
        template.append(container_model.image.image_tag)
        DockerClient.call(template)
