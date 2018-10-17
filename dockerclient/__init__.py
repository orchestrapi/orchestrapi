
import subprocess
from dataclasses import dataclass


@dataclass
class Container:
    def __init__(self, id, image, status, name):
        self.id = id
        self.image = image
        self.status = status
        self.name = name

    def __str__(self):
        return f"Container(id={self.id},name={self.name},status={self.status})"

    def __repr__(self):
        return self.__str__()

class DockerClient:

    @staticmethod
    def call(command):
        return subprocess.check_output(command).decode()

    @staticmethod
    def docker_ps():
        docker_ps_template = ["docker", "ps", "--format", '"{{.ID}}\t{{.Image}}\t{{.Status}}\t{{.Names}}"']
        result = DockerClient.call(docker_ps_template)
        result = [r.replace('"', '').split('\t') for r in result.split('\n') if r != '']
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
        print(template)
        result = DockerClient.call(template).replace('\n', '')
        print(result)

    @staticmethod
    def _stop(container_model):
        template = ['docker', 'stop', container_model.name]
        result = DockerClient.call(template).replace('\n', '')

    @staticmethod
    def _clean_image(container_model):
        template = ['docker', 'rm', '-f', container_model.name]

    @staticmethod
    def docker_start(container_model):
        if container_model.container_id:
            DockerClient._start(container_model)
        else:
            DockerClient._run(container_model)

    @staticmethod
    def _run(container_model):
        template = ["docker", "run"]
        if container_model.params != {}:
            for param in container_model.params.keys():
                template.append(f'-{param}')
                template.append(container_model.params[param])
        template.append('--name')
        template.append(container_model.name)
        template.append('-d')
        template.append(f'{container_model.image}:{container_model.version}')
        DockerClient.call(template).replace('\n', '')
