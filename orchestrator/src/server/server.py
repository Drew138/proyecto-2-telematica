import grpc
import concurrent

from protobuf import (
    register_pb2_grpc
)


class Server:
    def __init__(self, service, port) -> None:
        self.service = service
        self.port = port

    def start(self) -> None:
        print("Creando servidor GRPC", flush=True)
        thread_pool_ref = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        server = grpc.server(thread_pool_ref)
        register_pb2_grpc.add_RegisterServiceServicer_to_server(
            self.service, server)
        server.add_insecure_port(f'0.0.0.0:{self.port}')
        server.start()
        print("Servidor GRPC listo.\nListening...", flush=True)
        server.wait_for_termination()