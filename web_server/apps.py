from django.apps import AppConfig
from gRPS.client import run
import gRPS.grpc_server_pb2


class WebServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'web_server'

    def ready(self):
        run()
