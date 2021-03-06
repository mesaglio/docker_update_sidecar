import requests
import docker
from typing import Dict
from app.errors.docker import (
    ContainerNotFound,
    ErrorInContainer,
    ManyContainerWithImage,
)
from app.utils.bytes import parse_bytes

from app.utils.decorators import handler_exception


class DockerService:
    def __get_client__() -> docker.DockerClient:
        return docker.from_env()

    @classmethod
    def __get_container__(cls, container_id):
        return cls.__get_client__().containers.get(container_id)

    @classmethod
    def standar_container(cls, container) -> Dict:
        return {
            "id": container.id,
            "name": container.name,
            "state": container.status,
            "image": container.image.tags,
            "ports": container.ports,
        }

    @classmethod
    def get_containers(cls, only_running=False, image_name=""):
        filter = None
        if image_name:
            filter = {"ancestor": image_name}
        containers = cls.__get_client__().containers.list(
            all=not only_running, filters=filter
        )
        containers = list(
            map(lambda container: cls.standar_container(container), containers)
        )
        return containers

    @classmethod
    def run_container(cls, args):
        try:
            stdout = cls.__get_client__().containers.run(**args)
            if type(stdout) == bytes:
                return parse_bytes(stdout)
            return cls.standar_container(stdout)
        except Exception as e:
            raise ErrorInContainer(e.__str__())

    @classmethod
    def update_container_image(cls, old_image, container_args):
        try:
            old_containers = cls.get_containers(True, old_image)
            if len(old_containers) != 1:
                raise ManyContainerWithImage(
                    "There are many containers with the image."
                )
            old_container = old_containers[0]
            new_container = cls.run_container(container_args)
            cls.stop_container(old_container["id"])
            cls.remove_container(old_container["id"])
            return new_container
        except requests.exceptions.HTTPError:
            raise ContainerNotFound(old_image)

    @classmethod
    def start_container(cls, container_id):
        try:
            container = cls.__get_container__(container_id)
            container.start()
        except requests.exceptions.HTTPError:
            raise ContainerNotFound(container_id)

    @classmethod
    def stop_container(cls, container_id):
        try:
            container = cls.__get_container__(container_id)
            container.stop()
        except requests.exceptions.HTTPError:
            raise ContainerNotFound(container_id)

    @classmethod
    def remove_container(cls, container_id):
        try:
            container = cls.__get_container__(container_id)
            container.remove()
        except requests.exceptions.HTTPError:
            raise ContainerNotFound(container_id)

    @classmethod
    def get_logs(cls, container_id):
        try:
            return parse_bytes(cls.__get_container__(container_id).logs())
        except requests.exceptions.HTTPError:
            raise ContainerNotFound(container_id)

    @classmethod
    def get_container(cls, container_id):
        try:
            return cls.standar_container(cls.__get_container__(container_id))
        except requests.exceptions.HTTPError:
            raise ContainerNotFound(container_id)
