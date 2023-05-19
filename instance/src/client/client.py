from protobuf.register_pb2_grpc import (
    RegisterServiceStub,
    InstanceId,
)
import grpc
import time


class Client:

    def __init__(self, socket: str) -> None:
        self.socket = socket

    @staticmethod
    def safe_grpc_call(function):
        def inner(self, *args, **kwargs):
            for _ in range(10):
                try:
                    function()
                    return
                finally:
                    time.sleep(10)
        return inner

    @safe_grpc_call
    def register(self, instance_id: str) -> None:
        channel: grpc.Channel = grpc.insecure_channel(self.socket)
        self.register_stub: RegisterServiceStub = RegisterServiceStub(
            channel)
        
        payload: InstanceId = InstanceId(
            Id= instance_id
        )

        self.register_stub.Register(payload)
    
    @safe_grpc_call
    def unregister(self, instance_id: str) -> None:
        channel: grpc.Channel = grpc.insecure_channel(self.socket)
        self.register_stub: RegisterServiceStub = RegisterServiceStub(
            channel)

        payload: InstanceId = InstanceId(
            Id= instance_id
        )

        self.register_stub.Unregister(payload)



        
