from monitor.monitor import Monitor
from controller.controller import Controller
import threading
import time
import os


class Instance:

    instance_list = []
    lock = threading.Lock()

    def __init__(self, config: dict) -> None:
        self.instance_list.append(self)
        self.is_alive: bool = True
        self.is_asleep = True
        self.port: int = os.getenv('GRPC_PORT')
        self.config: dict = config
        self.controller: Controller = self.create_controller()
        self.sleep()
            

    def sleep(self):
        for _ in range(20):
            print("IN SLEEEP!!", flush=True)
            time.sleep(10)
            if not self.is_asleep:
                print("Instaced contacted, registered", flush=True)
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
    def remove_instance(cls, id) -> None:
        cls.lock.acquire()
        new_list: list[cls] = []

        print(id, flush=True)
        
        for instance in cls.instance_list:
            print()
            if instance.id == id:
                print(f"found instance to kill {instance.id}", flush=True)
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
            print("Monitor failed to start, deleting", flush=True)
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
            print("watch is alive", flush=True)
            self.monitor.ping()
            time.sleep(1)

    def watch_metric(self) -> None:
        while self.is_alive:
            print("watch metric", flush=True)
            self.monitor.update_metric()
            metric: int = self.monitor.get_metric()
            print("watch metric metric:",metric, flush=True)
            self.check_termination(metric)
            self.check_creation(metric)
            print("end watch metric", flush=True)
            time.sleep(20)

    def check_termination(self, metric: int) -> None:
        print("Check termination", flush=True)
        print("Metric", metric, flush=True)
        print("Delete policy", self.config['policy_config']['delete_policy'], flush=True)
        print("Number of current instances",Controller.instances, flush=True)
        print("Policy min instances", self.config['policy_config']['min_instances'], flush=True)
        if metric >= self.config['policy_config']['delete_policy']:
            return

        if Controller.instances <= self.config['policy_config']['min_instances']:
            return
        print("check termination failed, deleting", flush=True)
        self.remove_instance(self.id)

    def check_creation(self, metric: int) -> None:
        if metric <= self.config['policy_config']['create_policy']:
            return

        if Controller.instances >= self.config['policy_config']['max_instances']:
            return

        threading.Thread(target=Instance, args=[self.config]).start()
