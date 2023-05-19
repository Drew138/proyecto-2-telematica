import grpc
import concurrent.futures as futures
from protobuf import (
    register_pb2_grpc
)


class Server:
    def __init__(self, service, port) -> None:
        self.service = service
        self.port = port

    def start(self) -> None:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        register_pb2_grpc.add_RegisterServiceServicer_to_server(
            self.service, server)
        server.add_insecure_port(f'[::]:{self.port}')
        server.start()
        server.wait_for_termination()