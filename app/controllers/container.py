from app.service import docker
from app.utils.decorators import handler_exception
from flask_restx import Resource, reqparse, Namespace, Api

ns = Namespace("container", description="Containers endpoints")


@ns.route("/logs/<string:container_id>")
class ContainerLogs(Resource):
    @handler_exception
    def get(self, container_id):
        return docker.DockerService.get_logs(container_id)


@ns.route("/<string:container_id>")
class ContainerActions(Resource):
    @handler_exception
    def get(self, container_id):
        return docker.DockerService.get_container(container_id)

    @handler_exception
    def delete(self, container_id):
        docker.DockerService.stop_container(container_id)
        return {"success": True}

    @handler_exception
    def post(self, container_id):
        docker.DockerService.start_container(container_id)
        return {"success": True}


@ns.route("")
class Containers(Resource):
    @handler_exception
    @ns.doc("list_containers")
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "only_running", type=bool, help="Filter containers by status."
        )
        parser.add_argument("image_name", type=str, help="Filter containers by image.")
        args = parser.parse_args()
        return {
            "containers": docker.DockerService.get_containers(
                args["only_running"], args["image_name"]
            )
        }

    @handler_exception
    @ns.param("old_image", "Image to update")
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "old_image", type=str, help="Image to update.", required=True
        )
        args = parser.parse_args()
        container = docker.DockerService.update_container_image(
            args["old_image"], Api.payload
        )
        return {"container": container}

    @handler_exception
    def post(self):
        result = docker.DockerService.run_container(Api.payload)
        return {"result": result}
