import json


class Config:

    @staticmethod
    def create(file_path):
        with open(file_path, 'r') as f:
            config_dict = json.load(f)
            return config_dict
