from protobuf.register_pb2_grpc import (
    RegisterServiceStub,
)
from protobuf.register_pb2 import (
    InstanceId,
)
import grpc
import time


class Client:

    def __init__(self, socket: str) -> None:
        self.socket = socket

    def register(self, instance_id: str) -> None:
        channel: grpc.Channel = grpc.insecure_channel(self.socket)
        self.register_stub: RegisterServiceStub = RegisterServiceStub(
            channel)
        
        payload: InstanceId = InstanceId(
            id= instance_id
        )

        self.register_stub.Register(payload)
    
    def unregister(self, instance_id: str) -> None:
        channel: grpc.Channel = grpc.insecure_channel(self.socket)
        self.register_stub: RegisterServiceStub = RegisterServiceStub(
            channel)

        payload: InstanceId = InstanceId(
            id= instance_id
        )

        self.register_stub.Unregister(payload)



        
