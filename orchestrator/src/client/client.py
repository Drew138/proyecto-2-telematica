import grpc
# from orchestrator.src.protobuf import monitor_pb2
from google.protobuf import empty_pb2
from orchestrator.src.protobuf.monitor_pb2 import (
    monitor_pb2_grpc,
    PingResponse, 
    MetricResponse, 
    RegisterResponse,
)


class Client:

    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = monitor_pb2_grpc.MonitorServiceStub(channel)

    def is_alive(self):
        try:
            # Get the underlying channel object
            channel = stub.channel()

            # Check the connection state
            state = channel.state()

            # Return True if the connection is ready, False otherwise
            return state == grpc.ChannelConnectivity.READY

        except grpc.RpcError as e:
            # An error occurred, so the connection is not alive
            return True


    def Ping(self) -> bool:
        ping_result = self.stub.Ping(empty_pb2)
        return True

        
    def GetMetrics(self) -> int:
        metrics_result : MetricResponse = self.stub.GetMetrics(empty_pb2)
        return int(metrics_result.message)


    def Register(self):
        return self.stub.Register(empty_pb2)

    def Unregister(self):
        return self.stub.Unregister(empty_pb2)