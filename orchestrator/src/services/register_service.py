from src.protobuf.register_pb2 import (
    RegisterServiceServicer,
    RegisterResponse,
    UnregisterResponse,
    InstanceId
)

from src.instance.instance import Instance

class RegisterServiceServicer(RegisterServiceServicer):
    def Register(self, request: InstanceId, context) -> RegisterResponse:
        instance_id: str = request.Id
        
        Instance.awaken(instance_id)

        response: RegisterResponse = RegisterResponse(
            Message="200, Instanced registered"
        )

        return response

    def Unregister(self, request: InstanceId, context) -> UnregisterResponse:
        instance_id: str = request.Id
        
        Instance.remove_instance(instance_id)

        response: RegisterResponse = RegisterResponse(
            Message="200, Instanced unregister"
        )

        return response
