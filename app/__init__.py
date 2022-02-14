from flask import Flask
from flask_restx import Api
from app.controllers.container import ns as containerNs


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    api = Api(
        app,
        version="1.0",
        title="Container update api sidecar",
        description="A simple sidecar API to update containers images",
    )
    api.add_namespace(containerNs)
    return app
