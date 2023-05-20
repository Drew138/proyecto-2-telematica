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
        print(f"Creando instancia: IP={self.ip}, ID={self.id}", flush=True)
        self.sleep()
            

    def sleep(self):
        print(f"----> Iniciando espera de registro para IP={self.ip}", flush=True)
        for _ in range(20):
            time.sleep(10)
            if not self.is_asleep:
                print(f"--------> Instancia con IP={self.ip} se registro, iniciamos su monitoreo", flush=True)
                self.monitor: Monitor = self.create_monitor()
                self.start()
                return
        print("--------> Instancia no se registro en el tiempo dado, eliminando", flush=True)
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
        
        for instance in cls.instance_list:
            if instance.id == id:
                print(f"Eliminando instancia: IP={instance.ip}, ID={instance.id}", flush=True)
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
            print(f"Fallo en la creacion del monitor para instancia IP={self.ip}.\nEliminando", flush=True)
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
        print(f"Comienza checkeo por heartbeat a instancia {self.ip}", flush=True)
        while self.is_alive:
            self.monitor.ping()
            time.sleep(1)

    def watch_metric(self) -> None:
        while self.is_alive:
            print("======================", flush=True)
            print("======================", flush=True)
            print("Comienza analisis de metricas para ip", self.ip, flush=True)
            self.monitor.update_metric()
            metric: int = self.monitor.get_metric()
            print(f"----> Metrica consultada actualmente para instancia con ip {self.ip}:",metric, flush=True)
            self.check_termination(metric)
            self.check_creation(metric)
            print("======================", flush=True)
            print("======================", flush=True)
            time.sleep(30)

    def check_termination(self, metric: int) -> None:
        print("----------------------", flush=True)
        print(f"Comienza check para terminar instancia | Revisando a `{self.ip}`", flush=True)
        print(f"----> La metrica minima es {self.config['policy_config']['delete_policy']} y la actual es {metric}", flush=True)
        print(f"----> El minimo numero de instancias es {self.config['policy_config']['min_instances']} y la actual {Controller.instances}", flush=True)
        
        if metric >= self.config['policy_config']['delete_policy']:
            print(f"-------->La instancia cumple con el minimo de metrica", flush=True)
            return


        if Controller.instances <= self.config['policy_config']['min_instances']:
            print(f"--------> La instancia NO cumple con el minimo de metrica PERO llegamos al minimo de instancias", flush=True)
            return
        
        print(f"--------> Borrando instancia con ip {self.ip}", flush=True)
        self.remove_instance(self.id)

    def check_creation(self, metric: int) -> None:
        print("----------------------", flush=True)
        print(f"Comienza check para crear nueva instancia | Revisando a `{self.ip}`", flush=True)
        print(f"----> La metrica maxima es {self.config['policy_config']['delete_policy']} y la actual es {metric}", flush=True)
        print(f"----> El maximo numero de instancias es {self.config['policy_config']['min_instances']} y la actual {Controller.instances}", flush=True)
        
        if metric <= self.config['policy_config']['create_policy']:
            print(f"--------> La instancia cumple con el maximo de metrica", flush=True)
            return

        if Controller.instances >= self.config['policy_config']['max_instances']:
            print(f"--------> La instancia NO cumple con el maximo de metrica PERO llegamos al maximo de instancias", flush=True)
            return
        print(f"--------> Creando nueva instancia debido a que la intancia con ip {self.ip} sobrepasa condiciones requeridas", flush=True)
        threading.Thread(target=Instance, args=[self.config]).start()
