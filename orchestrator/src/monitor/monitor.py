from protobuf.monitor_pb2 import MetricResponse
from client.client import Client
from google.protobuf import empty_pb2

class Monitor:
    def __init__(self, instance) -> None:
        self.instance = instance
        self.client: Client = self._create_client()
        self.metric = 0

    def get_metric(self) -> int:
        return self.metric

    def get_instance(self):
        return self.instance

    def _create_client(self) -> Client:
        return Client(self.instance.get_socket())

    def ping(self) -> None:
        for _ in range(5):
            try:
                return_value = self.client.monitor_stub.Ping(empty_pb2.Empty())
                return return_value
            except Exception:
                pass
        instance = self.get_instance()
        return instance.remove_instance(instance.id)

    def update_metric(self) -> None:
        for _ in range(5):
            try:
                metric_response: MetricResponse = self.client.monitor_stub.GetMetrics()
                self.metric: int = metric_response.message
                return
            except Exception:
                pass
        instance = self.get_instance()
        return instance.remove_instance(instance.id)

    def application_failed_to_start(self) -> bool:
        return self.client.failed_to_start
