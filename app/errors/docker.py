from app.errors import GenericException


class ContainerNotFound(GenericException):
    def __init__(self, container_id):
        self.msg = f"Container with id: '{container_id}' not found."

class ImageNotFound(GenericException):
    def __init__(self, image_name):
        self.msg = f"Image name: {image_name} not found."
    
class ErrorInContainer(GenericException):
    def __init__(self, error_msg) -> None:
        self.msg = error_msg

class ManyContainerWithImage(GenericException):
    def __init__(self, error_msg) -> None:
        self.msg = error_msg