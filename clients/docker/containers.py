from django.template.defaultfilters import filesizeformat
from docker.errors import ImageNotFound, APIError, NotFound

from ..utils import clean_volume

class DockerContainerMixin:

    def ps(self):
        return self.client.containers.list()

    def _stop(self, container_instance):
        """Stops a container given its model."""
        container = self.client.containers.get(container_instance.container_id)
        container.stop()

    def container_id(self, container_instance):
        """Returns containers ID given the name."""
        from containers.models import Container
        if isinstance(container_instance, Container):
            field = container_instance.name
        else:
            field = container_instance.slug
        try:
            container = self.client.containers.get(field)
            return container.short_id
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
        except NotFound:
            print(f'Container {container_model.name} does not exists.')
        except APIError:
            print(f'Error removing container {container_model.name}.')

    def remove_image(self, image_model):
        """Removes an image."""

        try:
            image = self.client.images.get(image_model.image_id)
            image.remove()
        except CalledProcessError:
            print(f'Image {image_model.image_tag} does not exists.')
        except APIError:
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
                        template.append(clean_volume(volumen, container_model.app))
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
                        template.append(clean_volume(volumen. service_instance))
                else:
                    template.append(f'-{param}')
                    template.append(service_instance.params[param])
        template.append('--name')
        template.append(service_instance.slug)
        template.append('-d')
        template.append(service_instance.service_with_tag)
        self.remove(service_instance)
        self.call(template)

    def get_containers_on_network(self, network):
        network.reload()
        return network.containers

    def get_container_by_name(self, name):
        try:
            return self.client.containers.get(name)
        except NotFound:
            return None
        except APIError:
            print("Error obteniendo contenedor")
