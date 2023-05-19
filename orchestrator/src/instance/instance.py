from monitor.monitor import Monitor
from controller.controller import Controller
import threading
import time


class Instance:

    instance_list = []
    lock = threading.Lock()

    def __init__(self, config: dict) -> None:
        self.is_alive: bool = True
        self.is_asleep = True
        self.port: int = config['instance_config']['port']
        self.config: dict = config
        self.controller: Controller = self.create_controller()

        self.sleep()
            

    def sleep(self):
        for _ in range(20):
            print("IN SLEEEP!!", flush=True)
            time.sleep(10)
            if not self.is_asleep:
                self.monitor: Monitor = self.create_monitor()
                self.start()
                return
        print("KILLED INSTANCE", flush=True)
        Instance.remove_instance(self.id)

    @classmethod
    def awaken(cls, instance_id):
        for instance in cls.instance_list:
            if instance.id == instance_id:
                instance.is_asleep = False

    @classmethod
    def new(cls, config) -> None:
        cls.instance_list.append(cls(config))

    @classmethod
    def remove_instance(cls, id) -> None:
        cls.lock.acquire()
        new_list: list[cls] = []

        for instance in cls.instance_list:
            if instance.id == id:
                print(f"found instance to kill {instance.id}")
                instance.kill()
                instance.controller.delete_instance(instance.id)
            else:
                new_list.append(instance)

        cls.instance_list: list[cls] = new_list
        cls.lock.release()

    def create_controller(self) -> Controller:
        controller: Controller = Controller(self.config)
        self.id, self.ip = controller.create_instance()
        return controller

    def create_monitor(self) -> Monitor:
        monitor = Monitor(self)
        if monitor.application_failed_to_start():
            self.remove_instance(self.id)
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

        self.remove_instance(self.id)

    def check_creation(self, metric: int) -> None:
        if metric >= self.config['policy_config']['create_policy']:
            return

        if Controller.instances < self.config['policy_config']['max_instances']:
            return

        threading.Thread(target=self.new, args=[self.config]).start()
