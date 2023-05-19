from google.protobuf import empty_pb2
from monitor.monitor import Monitor
from protobuf.monitor_pb2 import (
    PingResponse,
    MetricResponse,
    RegisterResponse,
)
from protobuf import monitor_pb2_grpc


class MonitorServiceServicer(monitor_pb2_grpc.MonitorServiceServicer):
    def Ping(self, request: empty_pb2.Empty, context) -> PingResponse:
        return PingResponse(message='pong')

    def GetMetrics(self, request: empty_pb2.Empty, context) -> MetricResponse:
        load_metric = Monitor.get_metric()
        return MetricResponse(
            message=load_metric
        )

    def Register(self, request: empty_pb2.Empty, context) -> RegisterResponse:
        pass

    def Unregister(self, request: empty_pb2.Empty, context) -> RegisterResponse:
        pass
