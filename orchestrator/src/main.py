from config.config import Config
from orchestrator.src.common.instance import Instance


def main() -> None:
    config: dict = Config.create('./config.json')
    Instance.new(config)


if __name__ == '__main__':
    main()
