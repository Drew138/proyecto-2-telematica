from services.register_service import RegisterServiceServicer
from instance.instance import Instance
from server.server import Server
from config.config import Config
from flask import Flask
import threading
import os

app: Flask = Flask(__name__)

config: dict = Config.create('./config.json')


@app.route('/create')
def create() -> str:
    Instance.new(config)
    return 'Instance created successfully'


@app.route('/kill/<id>')
def kill(id) -> str:
    Instance.remove_instance(id)
    return 'Instance killed successfully'


def main() -> None:
    api_port = os.getenv('API_PORT')
    kwargs = {"host": "0.0.0.0", "port": api_port, "debug": True}
    threading.Thread(target=app.run, kwargs=kwargs).start()

    register_service = RegisterServiceServicer()
    grpc_port = os.getenv('GRPC_PORT')
    server = Server(register_service, grpc_port)
    server.start()

    threading.Thread(target=app.run).start()
    for _ in range(config['policy_config']['min_instances']):
        threading.Thread(target=Instance.new, args=[config]).start()


if __name__ == '__main__':
    main()
