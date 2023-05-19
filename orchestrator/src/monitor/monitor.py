from protobuf.monitor_pb2 import MetricResponse
from client.client import Client


class Monitor:
    def __init__(self, instance):
        self.instance = instance
        self.client: Client = self._create_client()

    def get_metric(self) -> int:
        return self.metric

    def get_instance(self):
        return self.instance

    def _create_client(self):
        return Client(self.instance.get_socket())

    @staticmethod
    def safe_grpc_call(function):
        def inner(self, *args, **kwargs):
            for _ in range(5):
                try:
                    return_value = function(self, *args, **kwargs)
                    return return_value
                except Exception:
                    pass
            instance = self.get_instance()
            return instance.remove_instance(instance.id)
        return inner

    @safe_grpc_call
    def ping(self):
        self.client.monitor_stub.Ping()

    @safe_grpc_call
    def update_metric(self):
        metric_response: MetricResponse = self.client.monitor_stub.GetMetrics()
        self.metric: int = metric_response.message

    def application_failed_to_start(self) -> bool:
        return self.client.failed_to_start
