import grpc
# from orchestrator.src.protobuf import monitor_pb2
from orchestrator.src.protobuf import monitor_pb2_grpc
from google.protobuf import empty_pb2


class Client:

    def __init__(self, address):
        channel = grpc.insecure_channel(address)
        self.stub = monitor_pb2_grpc.MonitorServiceStub(channel)

    def Ping(self):
        return self.stub.Ping(empty_pb2)
        
    def GetMetrics(self):
        return self.stub.GetMetrics(empty_pb2)

    def Register(self):
        return self.stub.Register(empty_pb2)

    def Unregister(self):
        return self.stub.Unregister(empty_pb2)