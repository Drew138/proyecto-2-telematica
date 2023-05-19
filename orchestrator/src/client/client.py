from protobuf.monitor_pb2_grpc import MonitorServiceStub
import grpc
import time
from google.protobuf import empty_pb2


class Client:

    def __init__(self, socket: str) -> None:
        self.failed_to_start: bool = False
        self.start(socket)

    def start(self, socket: str) -> None:
        # for _ in range(10):
        try:
            print("SOCKET", socket, flush=True)
            channel: grpc.Channel = grpc.insecure_channel(socket)
            self.monitor_stub: MonitorServiceStub = MonitorServiceStub(
                channel)
            self.monitor_stub.Ping(empty_pb2.Empty())
            return
        except grpc.RpcError as rpc_error:
            print("Failed to connect in create client", flush=True)
            self.failed_to_start: bool = True
        finally:
            time.sleep(10)

