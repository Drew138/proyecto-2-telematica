from orchestrator.src.common.instance import Instance
from orchestrator.src.common.error import Error
from orchestrator.src.client.client import Client
import boto3


class Monitor:
    def __init__(self, instance: Instance):
        self.instance: Instance = instance
        self.metric: int = 0
        self.grpc_client = self.create_grpc_client()

    # Public
    def get_metric(self) -> int:
        return self.metric
    
    def get_instance(self) -> Instance:
        return self.instace
    
    # Internal
    def create_grpc_client(self):
        instance_id = self.instace.get_id()
        instance_ip = self.instace.get_ip()

        # Now create the client
        return Client(instance_ip)

    def ping(self) -> Error: # Error
        # Check if instance is running with boto3
        # TODO:

        # Check if GRPC conn is alive
        err = self.grpc_client.is_alive()

        if err:
            return Err('GRPC connection not alive')
        
        self.grpc_client.Ping()

        return None 

    def update_metric(self) -> Error:
        
        # Check if GRPC conn is alive
        err = self.grpc_client.is_alive()

        if err:
            return Err('GRPC connection not alive')

        # Get the metric
        new_metric = self.grpc_client.GetMetrics()

        self.metric = new_metric

        return None 
    
    def try_function(self, function) -> Error:

        def inner():
            tries = 1
            while True:
                err = function()

                if not err: # Function returned no Errors
                    break

                if err and tries < SELF.MAX_TRIES:
                    sleep(self.INTERVAL) # TODO: definir otro intervalo de nuevo intento
                    tries += 1
                else:
                    return Error("Maximum connection tries exceeded")
                
            return None
                
        return inner


    def check(self) -> Error: # Err
        err = self.try_function(self.ping)

        if err:
            return err
        
        err = self.try_function(self.update_metric())

        if err:
            return err
    
        return None



        
