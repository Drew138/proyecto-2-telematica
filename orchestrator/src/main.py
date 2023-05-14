from orchestrator.src.instance.instance import Instance
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
    for _ in range(config['policy_config']['min_instances']):
        threading.Thread(target=Instance.new, args=[config]).start()


if __name__ == '__main__':
    main()
