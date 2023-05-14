from google.protobuf import empty_pb2
from controller.src.protobuf.register_pb2 import (
    RegisterResponse,
    UnregisterResponse,
)
from controller.src.protobuf import register_pb2_grpc


class RegisterServiceServicer(register_pb2_grpc.RegisterServiceServicer):
    def Register(self, request: empty_pb2.Empty, context) -> RegisterResponse:
        pass

    def Unregister(self, request: empty_pb2.Empty, context) -> UnregisterResponse:
        pass
