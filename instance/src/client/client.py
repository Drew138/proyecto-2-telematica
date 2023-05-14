from protobuf.register_pb2_grpc import RegisterServiceStub
import grpc
import time


class Client:

    def __init__(self, socket: str) -> None:
        self.register(socket)

    def register(self, socket: str) -> None:
        for _ in range(10):
            try:
                channel: grpc.Channel = grpc.insecure_channel(socket)
                self.register_stub: RegisterServiceStub = RegisterServiceStub(
                    channel)
                self.register_stub.Register()
                return
            finally:
                time.sleep(10)
    
    def unregister(self, socket: str) -> None:
        channel: grpc.Channel = grpc.insecure_channel(socket)
        self.register_stub: RegisterServiceStub = RegisterServiceStub(
            channel)
        self.register_stub.Unregister()


        
