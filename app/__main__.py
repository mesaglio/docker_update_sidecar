from flask import Flask
from flask_restx import Resource, Api, reqparse
from app.service import docker
from app.utils.decorators import handler_exception

app = Flask(__name__)
app.url_map.strict_slashes = False
api = Api(
    app,
    version="1.0",
    title="Container update apsidecar",
    description="A simple sidecar API to update containers images",
)


@api.route("/container/logs/<string:container_id>")
class ContainerLogs(Resource):
    @handler_exception
    def get(self, container_id):
        return docker.DockerService.get_logs(container_id)


@api.route("/container/<string:container_id>")
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


@api.route("/container")
class Containers(Resource):
    @handler_exception
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
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "old_image", type=str, help="Image to update.", required=True
        )
        args = parser.parse_args()
        container = docker.DockerService.update_container_image(
            args["old_image"], api.payload
        )
        return {"container": container}

    @handler_exception
    def post(self):
        result = docker.DockerService.run_container(api.payload)
        return {"result": result}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
