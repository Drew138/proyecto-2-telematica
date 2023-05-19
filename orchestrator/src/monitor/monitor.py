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
        for _ in range(5):
            try:
                return_value = self.client.monitor_stub.Ping(empty_pb2.Empty())
                return return_value
            except Exception:
                pass
        instance = self.get_instance()
        print("Calling remove from ping in monitor", flush=True)
        instance.remove_instance(instance.id)
        return 

    def update_metric(self) -> None:
        for _ in range(5):
            try:
                metric_response: MetricResponse = self.client.monitor_stub.GetMetrics(empty_pb2.Empty())
                self.metric: int = metric_response.message
                return
            except Exception as e:
                print("Error:",e, flush=True)
                print("Error ocurrio en update metric", flush=True)
                pass
        instance = self.get_instance()
        print("Borrando desde update metric", flush=True)
        return instance.remove_instance(instance.id)

    def application_failed_to_start(self) -> bool:
        return self.client.failed_to_start
