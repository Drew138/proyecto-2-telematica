from protobuf.monitor_pb2 import MetricResponse
from client.client import Client
from google.protobuf import empty_pb2
import threading



class Monitor:
    def __init__(self, instance) -> None:
        self.instance = instance
        self.client: Client = self._create_client()
        self.metric = 15

    def get_metric(self) -> int:
        return self.metric

    def get_instance(self):
        return self.instance

    def _create_client(self) -> Client:
        c = Client(self.instance.get_socket())
        return c

    def ping(self) -> None:
        instance = self.get_instance()
        print(f"Intentando pingear a IP={instance.ip}")
        for _ in range(5):
            try:
                return_value = self.client.monitor_stub.Ping(empty_pb2.Empty())
                return return_value
            except Exception:
                print("Error ocurrio en ping", flush=True)
                pass
        
        print(f"Fallo Pingeando a IP={instance.ip}.\nEliminando instancia", flush=True)
        instance.remove_instance(instance.id)
        return 

    def update_metric(self) -> None:
        instance = self.get_instance()
        print(f"Intentando conseguir metrica de IP={instance.ip}")
        for _ in range(5):
            try:
                metric_response: MetricResponse = self.client.monitor_stub.GetMetrics(empty_pb2.Empty())
                self.metric: int = metric_response.message
                return
            except Exception as e:
                print("Error ocurrio en update metric", flush=True)
                pass
        
        print(f"Fallo conseguir metrica de IP={instance.ip}.\nEliminando instancia", flush=True)
        return instance.remove_instance(instance.id)

    def application_failed_to_start(self) -> bool:
        return self.client.failed_to_start
