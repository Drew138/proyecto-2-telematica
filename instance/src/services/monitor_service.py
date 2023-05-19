from google.protobuf import empty_pb2
from monitor.monitor import Monitor
from protobuf.monitor_pb2 import (
    PingResponse,
    MetricResponse,
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

