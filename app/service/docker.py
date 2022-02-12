import requests
import docker
from typing import Dict
from app.errors.docker import ContainerNotFound, ErrorInContainer

from app.utils.decorators import handler_exception

class DockerService:
    def __get_client__() -> docker.DockerClient:
        return docker.from_env()

    @classmethod
    def standar_container(cls, container) -> Dict:
        return {
            'id': container.id,
            'name': container.name,
            'state': container.status,
            'image': container.image.tags,
            'ports': container.ports
        }

    @classmethod
    def get_running_containers(cls):
        containers = cls.__get_client__().containers.list(all=True)
        containers = list(map(lambda container: cls.standar_container(container), containers))
        return containers
    
    @classmethod
    def run_container(cls, args):
        try:
            stdout = cls.__get_client__().containers.run(**args)
            if type(stdout) == bytes:
                stdout = stdout.decode('utf-8')
                if '\n' in stdout:
                    stdout = stdout.split('\n')
                return stdout
            return cls.standar_container(stdout)
        except Exception as e:
            raise ErrorInContainer(e.__str__())
    
    @classmethod
    def start_container(cls, container_id):
        try:
            container = cls.__get_client__().containers.get(container_id)
            container.start()
        except requests.exceptions.HTTPError:
            raise ContainerNotFound(container_id)

    @classmethod
    def stop_container(cls, container_id):
        try:
            container = cls.__get_client__().containers.get(container_id)
            container.stop()
        except requests.exceptions.HTTPError:
            raise ContainerNotFound(container_id)

    @classmethod
    def remove_container(cls, container_id):
        try:
            container = cls.__get_client__().containers.get(container_id)
            container.remove()
        except requests.exceptions.HTTPError:
            raise ContainerNotFound(container_id)

    @classmethod
    def get_container(cls, container_id):
        try:
            return cls.standar_container(cls.__get_client__().containers.get(container_id))
        except requests.exceptions.HTTPError:
            raise ContainerNotFound(container_id)