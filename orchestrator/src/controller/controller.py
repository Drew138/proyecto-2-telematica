import boto3


class Controller:

    instances: int = 0

    def __init__(self, config: dict) -> None:
        ip = config['orchestrator_config']['ip_address']
        self.instance_config = config["instance_config"]
        self._set_ec2_client(config["auth_config"])
        self. user_data = f'''#!/bin/bash
        echo ORCHESTRATOR_IP={ip} SELF_ID=$(ec2metadata --instance-id) | tr ' ' '\n' > /home/ubuntu/proyecto-2-telematica/.env
        sudo docker-compose -f /home/ubuntu/proyecto-2-telematica/docker-compose.instance.yml up -d
        '''
    
    @classmethod
    def increase_instances(cls) -> None:
        cls.instances += 1

    @classmethod
    def decrease_instances(cls) -> None:
        cls.instances -= 1

    
    def _set_ec2_client(self, auth_config: dict) -> None:
        self.ec2_client = boto3.client(
            'ec2',
            aws_access_key_id=auth_config["aws_access_key_id"],
            aws_secret_access_key=auth_config["aws_secret_access_key"],
            aws_session_token=auth_config["aws_session_token"],
            region_name=auth_config["region_name"],
        )

    def create_instance(self) -> tuple[str, str]:
        response = self.ec2_client.run_instances(
            ImageId=self.instance_config["ami_id"],
            UserData=self.user_data,
            InstanceType=self.instance_config["instance_type"],
            KeyName=self.instance_config["key_pair_name"],
            SecurityGroupIds=self.instance_config["security_group_ids"],
            MinCount=1,
            MaxCount=1
        )
        instance = response['Instances'][0]
        instance_id = instance['InstanceId']
        instance_ip = instance['PrivateIpAddress']
        Controller.increase_instances()
        return instance_id, instance_ip

    def delete_instance(self, instance_id: str) -> None:
        self.ec2_client.terminate_instances(
            InstanceIds=[instance_id]
        )
        Controller.decrease_instances()

