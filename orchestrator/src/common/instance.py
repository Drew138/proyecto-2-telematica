from orchestrator.src.monitor.monitor import Monitor
from orchestrator.src.controller.controller import Controller
import threading
import time


class Instance:
    def __init__(self, config: dict) -> None:
        self.is_alive: bool = True
        self.port: int = config['instance_config']['port']
        self.config: dict = config
        self.controller: Controller = self.create_controller()
        self.monitor: Monitor = self.create_monitor()
        self.start()

    @classmethod
    def new(cls, config) -> None:
        cls(config)

    def create_controller(self) -> Controller:
        controller: Controller = Controller(self.config)
        self.id, self.ip = controller.create_instance()
        return controller

    def create_monitor(self) -> Monitor:
        monitor = Monitor(self)
        if monitor.application_failed_to_start():
            self.kill()
        return monitor

    def kill(self) -> None:
        self.is_alive: bool = False

    def get_socket(self) -> str:
        return f'{self.ip}:{self.port}'

    def start(self) -> None:
        threading.Thread(target=self.watch_connection).start()
        threading.Thread(target=self.watch_metric).start()

    def watch_connection(self) -> None:
        while self.is_alive:
            self.monitor.ping()
            time.sleep(1)
        self.controller.delete_instance(self.id)

    def watch_metric(self) -> None:
        while self.is_alive:
            self.monitor.update_metric()
            metric: int = self.monitor.get_metric()
            self.check_termination(metric)
            self.check_creation(metric)
            time.sleep(20)

    def check_termination(self, metric: int) -> None:
        if metric <= self.config['policy_config']['delete_policy']:
            return

        if Controller.instances > self.config['policy_config']['min_instances']:
            return

        self.kill()

    def check_creation(self, metric: int) -> None:
        if metric >= self.config['policy_config']['create_policy']:
            return

        if Controller.instances < self.config['policy_config']['max_instances']:
            return

        threading.Thread(target=self.new, args=[self.config]).start()
