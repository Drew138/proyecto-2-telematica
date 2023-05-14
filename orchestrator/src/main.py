from orchestrator.src.common.instance import Instance
from config.config import Config
from flask import Flask
import threading

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
    threading.Thread(target=app.run).start()
    Instance.new(config)


if __name__ == '__main__':
    main()
