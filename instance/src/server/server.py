import grpc
import futures
from node.src.handler.handler import MonitorServiceServicer
from node.src.protobuf.monitor_pb2 import (
    monitor_pb2_grpc,
)

class Server:
    def __init__(self, _handler):
        self.HANDLER = _handler
        self.PORT = 20 # TODO: READ
    
    def start(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        monitor_pb2_grpc.add_RouteGuideServicer_to_server(
            self.HANDLER, server)
        server.add_insecure_port(f'[::]:{self.PORT}')
        server.start()
        server.wait_for_termination()