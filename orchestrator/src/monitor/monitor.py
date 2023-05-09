from orchestrator.src.common.instance import Instance
from orchestrator.src.client.client import Client
import boto3


class Monitor:
    def __init__(self, instance: Instance):
        self.instance: Instance = instance
        self.metric: int = 0
        self.grpc_client = = self.create_grpc_client()

    # Public
    def get_metric(self) -> int:
        return self.metric
    
    def get_instance(self) -> Instance:
        return self.instace
    
    # Internal
    def create_grpc_client(self):
        instance_id = self.instace.get_id()
        instance_ip = self.instace.get_ip()

        # Create a resource
        ec2_resource = boto3.resource('ec2')

        # Wait until creation before establishing connection
        instance = ec2_resource.Instance(instance_id)
        instance.wait_until_running()

        # Now create the client
        return Client(instance_ip)

    def ping(self) -> bool: # Error
        # Check EC2 status with BOTO3
        # Then ping with GRPC
        # return False # Err
        return False  # Done

    def update_metric(self) -> bool: # Metric, Err
        # return 0, True # Err
        return False # Done 
    
    def try_function(self, function) -> bool:

        def inner():
            tries = 1
            while True:
                err = function()

                if err == False: # Good ping
                    break

                if err and tries < SELF.MAX_TRIES:
                    sleep(self.INTERVAL) #TODO: definir otro intervalo de nuevo intento
                    tries += 1
                else:
                    return False
        
        return inner


    def check(self) -> bool: # Err
        # We try to ping some times 
        # before saying the instace is down
        
        err = self.try_function(self.ping)

        if err:
            return False
        
        err = self.try_function(self.update_metric())

        if err:
            return False
    
        return True



        
