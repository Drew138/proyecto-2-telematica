from instance.src.handler.handler import Handler
from instance.src.monitor.monitor import Monitor
from instance.src.server.server import Server


def main():
    print("Starting monitor instance...")

    # Start the monitor
    monitor = Monitor()
    print("Monitor class created")

    # Start the endpoint handler and set the monitor
    handler = Handler()
    handler.setMonitor(monitor)
    print("Handler created")

    # Start the server
    server = Server()
    server.start()
    print("GRPC server started")

    print("Configuration finished")
    print("Instance is listening")


if __name__ == "__main__":
    main()
