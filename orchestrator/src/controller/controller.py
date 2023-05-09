import boto3
from time import sleep


class Controller:

    class Instance:
        def __init__(self, id: str, ip: str):
            self.is_alive = True
            self.id = id
            self.ip = ip

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
        return self.Instance(instance_id, instance_ip)

    def delete_instance(self, instance: Instance):
        response = self.ec2_client.terminate_instances(
            InstanceIds=[instance.id]
        )

    def modify_instance(self):
        pass

    def read_metrics(self):
        pass

    def decide(self, ip: str, metric: int) -> str:
        response = ""
        if metric > self.CREATE_METRIC:
            if self.instances < self.MAX_INSTANCES:
                self.create_node()
                self.instances += 1
                response = f"New node created. Total instances: {self.instances}"
            else:
                response = "Maximum number of nodes reached, can't create more"
        elif metric < self.DELETE_METRIC:
            if self.instances > self.MIN_INSTANCES:
                self.delete_node(ip)
                self.instances -= 1
                response = f"Deleted node {ip}. Total instances: {self.instances}"
            else:
                response = "Minimum number of nodes reached, can't delete more"

        return f"Node {ip}: Okay" if response == "" else response

    def manager(self):
        while True:
            # Wait before executing
            sleep(self.INTERVAL)

            # Analyze
            metrics = self.read_metrics()
            for data in metrics:
                ip = data.ip
                metric = data.metric

                result = self.decide(ip, metric)
                print(result)
