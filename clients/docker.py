"""Docker client module."""
import json
import subprocess
from subprocess import CalledProcessError

import docker
from django.conf import settings
from django.template.defaultfilters import filesizeformat
from docker.errors import ImageNotFound, NotFound

from . import ShellClient
from .git import GitClient as gclient
from .tasks import send_slack_message


class DockerClient:

    """Special client for docker commands."""

    def __init__(self):
        self.client = docker.from_env()

    def call(self, command):
        """Call method to execute shell commands."""
        return subprocess.check_output(command).decode()

    def ps(self):
        return self.client.containers.list()

    def _stop(self, container_instance):
        """Stops a container given its model."""
        container = self.client.containers.get(container_instance.container_id)
        container.stop()

    def container_id(self, container_instance):
        """Returns containers ID given the name."""
        try:
            container = self.client.containers.get(container_instance.name)
            return container.short_id
        except NotFound:
            return None

    def service_id(self, service_instance):
        """Returns containers ID given the name."""
        try:
            service = self.client.containers.get(service_instance.slug)
            return service.short_id
        except NotFound:
            return None

    def container_status(self, container_id):
        """Returns status of a given container by id."""
        try:
            container = self.client.containers.get(container_id)
            return container.status
        except NotFound:
            return None

    def _start(self, container_instance):
        """Start command given the container name."""
        try:
            container = self.client.containers.get(
                container_instance.container_id)
        except NotFound:
            return None
        container.start()

    def pull_from_dockerhub(self, image_name):
        """Pulls an image from docker hub."""
        return self.client.images.pull(image_name)

    def image_id(self, image_name):
        """Returns an image id given its name."""
        try:
            image = self.client.images.get(image_name)
            return image.short_id
        except ImageNotFound:
            return None

    def image_id_and_size(self, image_name):
        """Returns a tuble with image id and size, given the image name."""
        try:
            image = self.client.images.get(image_name)
            return image.short_id, filesizeformat(image.attrs['Size']).replace('\xa0', '')
        except ImageNotFound:
            return None

    def inspect(self, container_model):
        """Returns container meta data."""
        container = self.client.containers.get(container_model.container_id)
        return container.attrs

    def docker_start(self, container_model, instance_name=None):
        """Starts a container with 'start' command if it exists, 'run' it if not."""
        if container_model.container_id:
            self._start(container_model)
        else:
            from services.models import Service
            if isinstance(container_model, Service):
                self._run_service(container_model)
            else:
                self._run(container_model, instance_name=instance_name)

    def remove(self, container_model):
        """Removes a container."""

        try:
            container = self.client.containers.get(
                container_model.name)
            container.remove()
        except docker.errors.NotFound:
            print(f'Container {container_model.name} does not exists.')
        except docker.errors.APIError:
            print(f'Error removing container {container_model.name}.')

    def remove_image(self, image_model):
        """Removes an image."""

        try:
            image = self.client.images.get(image_model.image_id)
            image.remove()
        except CalledProcessError:
            print(f'Image {image_model.image_tag} does not exists.')
        except docker.errors.APIError:
            print(f'Error removing container {container_model.name}.')

    def _run(self, container_model, instance_name=None):
        """Runs a container using 'run' command."""
        template = ["docker", "run"]
        if container_model.params != {}:
            for param in container_model.params.keys():
                if param == 'e':
                    for par_e, par_e_val in container_model.params['e'].items():
                        template.append(f'-{param}')
                        template.append(f'{par_e}={par_e_val}')
                elif param == 'v' or param == 'p':
                    for volumen in container_model.params[param]:
                        template.append(f'-{param}')
                        template.append(volumen)
                else:
                    template.append(f'-{param}')
                    template.append(container_model.params[param])
        template.append('--name')
        template.append(instance_name or container_model.name)
        template.append('-d')
        template.append(container_model.image.image_tag)
        self.remove(container_model)
        self.call(template)

    def _run_service(self, service_instance):
        """Runs a service container using 'run' command."""
        template = ["docker", "run"]
        if service_instance.params != {}:
            for param in service_instance.params.keys():
                if param == 'e':
                    for par_e, par_e_val in service_instance.params['e'].items():
                        template.append(f'-{param}')
                        template.append(f'{par_e}={par_e_val}')
                elif param == 'v' or param == 'p':
                    for volumen in service_instance.params[param]:
                        template.append(f'-{param}')
                        template.append(volumen)
                else:
                    template.append(f'-{param}')
                    template.append(service_instance.params[param])
        template.append('--name')
        template.append(service_instance.slug)
        template.append('-d')
        template.append(service_instance.service_with_tag)
        self.remove(service_instance)
        self.call(template)

    def build_from_image_model(self, image, git_name):
        """Builds a container using an Image instance."""
        if not image.app.cloned:
            send_slack_message.delay('clients/slack/message.txt', {
                'message': f'Va clonarse la app *{image.name}:{image.tag}*'
            })
            gclient.clone(image.app)
            image.app.data['cloned'] = True
            image.app.save()

        gclient.checkout_tag(git_name, image.tag)
        send_slack_message.delay('clients/slack/message.txt', {
            'message': f'Va construirse la imagen *{image.name}:{image.tag}*'
        })
        template = [
            'docker', 'build', '-t',
            f'{image.image_tag}',
            f'{settings.GIT_PROJECTS_ROUTE}/{git_name}/.']
        return self.call(template)

    def create_network(self, name):
        return self.client.networks.create(name, driver="bridge")

    def remove_network(self, network):
        try:
            network.remove()
        except docker.errors.APIError:
            print(f"Error al eliminar la red {network.id}")

    def get_network_by_id(self, network_id, verbose=False):
        try:
            return self.client.networks.get(network_id, verbose=verbose)
        except docker.errors.NotFound:
            return None
        except docker.errors.APIError:
            print(f"Error obteniendo red {network_id}")

    def connect_container_to_network(self, network, container):
        try:
            network.connect(container)
        except docker.errors.APIError:
            print(
                f"Error conectando contenedor {container} a la red {network.name}")

    def disconnect_container_to_network(self, network, container, force=False):
        try:
            network.disconnect(container, force=force)
        except docker.errors.APIError:
            print(
                f"Error desconectando contenedor {container} a la red {network.name}")

    def list_networks(self):
        try:
            return self.client.networks.list()
        except docker.errors.APIError:
            print("Error al listar redes")

    def networks_prune(self, filters=None):
        try:
            return self.client.networks.prune(filters=filters)
        except docker.errors.APIError:
            print("Error borrando redes sin uso")

    def get_containers_on_network(self, network):
        network.reload()
        return network.containers

    def get_container_by_name(self, name):
        try:
            return self.client.containers.get(name)
        except docker.errors.NotFound:
            return None
        except docker.errors.APIError:
            print("Error obteniendo contenedor")