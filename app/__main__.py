from flask import Flask
from flask_restx import Resource, Api
from app.service import docker
from app.utils.decorators import handler_exception

app = Flask(__name__)
api = Api(app)

@api.route('/container/<string:container_id>')
class ContainerActions(Resource):
    @handler_exception
    def get(self, container_id):
        return docker.DockerService.get_container(container_id)
    
    @handler_exception
    def delete(self, container_id):
        docker.DockerService.stop_container(container_id)
        return {'success': True}
    
    @handler_exception
    def post(self, container_id):
        docker.DockerService.start_container(container_id)
        return {'success': True}

@api.route('/container')
class Containers(Resource):
    @handler_exception
    def get(self):
        return {'containers': docker.DockerService.get_running_containers()}
    
    @handler_exception
    def post(self):
        result = docker.DockerService.run_container(api.payload)
        return {'result': result}

if __name__ == '__main__':
    app.run(debug=True)