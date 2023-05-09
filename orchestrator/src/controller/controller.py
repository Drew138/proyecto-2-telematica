import boto3
from time import sleep
from orchestrator.src.common import Instance


class Controller:
    def __init__(self, ENV_VARS, config):
        # Env

        # self.CREATE_METRIC = 0  # TODO
        # self.DELETE_METRIC = 0  # TODO
        # self.MAX_INSTANCES = 0  # TODO
        # self.MIN_INSTANCES = 0  # TODO
        # self.INTERVAL

        # Self
        self.instances = 0

        self.instance_policy_config = config["instance_policy_config"]
        self.auth_config = config["auth_config"]
        self.instance_config = config["instance_config"]
        self._set_ec2_client()


    # AWS functions
    def _set_ec2_client(self):
        self.ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=self.instance_config["aws_access_key_id"],
            aws_secret_access_key=self.instance_config["aws_secret_access_key"],
            aws_session_token=self.instance_config["aws_session_token"],
            region_name=self.instance_config["region_name"],
        )

    def create_instance(self) -> Instance:
        response = self.ec2_client.run_instances(
            ImageId=self.instance_config["ami_id"],
            InstanceType=self.instance_config["instance_type"],
            KeyName=self.instance_config["key_pair_name"],
            SecurityGroupIds=self.instance_config["security_group_id"],
            MinCount=1,
            MaxCount=1
        )
        instance = response['Instances'][0]
        instance_id = instance['InstanceId']
        instance_ip = instance['PrivateIpAddress']
        return Instance(instance_id, instance_ip)

    def delete_instance(self, instance: Instance):
        response = self.ec2_client.terminate_instances(
            InstanceIds=[instance.id]
        )
    
    # Internal functions
    def new_instance(self) -> bool: 
        if self.instances >= self.MAX_INSTANCES:
            print("Maximum number of instances reached, can't create more")
            return True

        # Create a new instace
        instance = self.create_instance()

        # Create a monitor for the instance
        monitor = Monitor(instance)

        # Increase instance count
        self.instances += 1

        # Start deciding on the monitor data
        decide = threading.Thread(target=self.decide, args=(monitor))
        decide.start()

        print(f"New instance created. Total instances: {self.instances}")
        return False

    def remove_instance(self, monitor: Monitor) -> bool:
        instance = monitor.get_instance()

        if self.instances <= self.MIN_INSTANCES:
            print("Minimum number of instances reached, can't delete more")
            return True

        # Delete the instance
        self.delete_instance(instance)

        # Delete its monitor
        del monitor

        # Decrease the instance count
        self.instances -= 1

        print(f"Deleted instance {ip}. Total instances: {self.instances}")
        return False

    def manager(self, monitor):
        while True:
            # Wait before executing
            sleep(self.INTERVAL)

            # Check instance metric, ask for ping and metrics
            err = monitor.check()

            # Error: Intentamos pingear varias veces sin exito
            # Instancia caida
            if err:
                self.remove_instance(monitor)
                break

            metric = monitor.get_metric()
            ip = monitor.get_instance().get_ip()
            
            result = ""
            if metric > self.CREATE_METRIC:
                err = self.new_instance()
            elif metric < self.DELETE_METRIC:
                err =self.remove_instance(monitor)
                break
            else:
                print(f"Node {ip}: Okay")
                
            
