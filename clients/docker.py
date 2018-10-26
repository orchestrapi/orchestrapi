
import json
from .helpers import Container
from . import ShellClient

class DockerClient(ShellClient):

    @staticmethod
    def docker_ps():
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
        running_containers = DockerClient.docker_ps()
        for container in running_containers:
            if container.id == container_id:
                return container.status
        return None

    @staticmethod
    def container_id(container_name):
        running_containers = DockerClient.docker_ps()
        for container in running_containers:
            if container.name == container_name:
                return container.id
        return None

    @staticmethod
    def _start(container_model):
        template = ['docker', 'start', container_model.name]
        return DockerClient.call(template).replace('\n', '')

    @staticmethod
    def _stop(container_model):
        template = ['docker', 'stop', container_model.name]
        return DockerClient.call(template).replace('\n', '')

    @staticmethod
    def remove(container_model):
        template = ['docker', 'rm', '-f', container_model.container_id]
        DockerClient.call(template)

    @staticmethod
    def _clean_image(container_model):
        template = ['docker', 'rm', '-f', container_model.name]

    @staticmethod
    def docker_start(container_model, instance_name=None):
        if container_model.container_id:
            DockerClient._start(container_model)
        else:
            DockerClient._run(container_model, instance_name=instance_name)

    @staticmethod
    def inspect(container_model):
        template = ['docker', 'inspect', container_model.name]
        response = DockerClient.call(template)
        return json.loads(response)[0]

    @staticmethod
    def _run(container_model, instance_name=None):
        template = ["docker", "run"]
        if container_model.params != {}:
            for param in container_model.params.keys():
                if param == 'e':
                    for par_e, par_e_val in container_model.params['e'].items():
                        template.append(f'-{param}')
                        template.append(f'{par_e}={par_e_val}')
                else:
                    template.append(f'-{param}')
                    template.append(container_model.params[param])
        template.append('--name')
        template.append(instance_name or container_model.name)
        template.append('-d')
        template.append(f'{container_model.image}:{container_model.version}')
        DockerClient.call(template).replace('\n', '')
