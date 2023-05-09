from google.protobuf import empty_pb2
from node.src.monitor.monitor import Monitor
from node.src.protobuf.monitor_pb2 import (
    monitor_pb2_grpc,
    PingResponse, 
    MetricResponse, 
    RegisterResponse,
)

class MonitorServiceServicer(monitor_pb2_grpc.MonitorServiceServicer):
    def setMonitor(self, _monitor: Monitor):
        self.monitor = _monitor

    def Ping(self, request: empty_pb2.Empty, context) -> PingResponse:
        status = self.monitor.heartbeat()
        res = PingResponse(
            message = status
        )
        return res
    
    def GetMetrics(self, request: empty_pb2.Empty, context) -> MetricResponse:
        load_metric = self.monitor.get_metrics()
        res = MetricResponse(
            message = load_metric
        )
        return res
    
    def Register(self, request: empty_pb2.Empty, context) -> RegisterResponse:
        pass
    
    def Unregister(self, request: empty_pb2.Empty, context) -> RegisterResponse:
        pass