from protobuf.register_pb2 import (
    RegisterResponse,
    UnregisterResponse,
    InstanceId
)

from instance.instance import Instance
from protobuf import register_pb2_grpc


class RegisterServiceServicer(register_pb2_grpc.RegisterServiceServicer):
    def Register(self, request: InstanceId, context) -> RegisterResponse:
        instance_id: str = request.id

        Instance.awaken(instance_id)

        response: RegisterResponse = RegisterResponse(
            message="200, Instanced registered"
        )

        return response

    def Unregister(self, request: InstanceId, context) -> UnregisterResponse:
        instance_id: str = request.id

        Instance.remove_instance(instance_id)

        response: UnregisterResponse = UnregisterResponse(
            message="200, Instanced unregister"
        )

        return response
