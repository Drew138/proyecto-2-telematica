import json

# Lee los criterios de creacion y elminado de nodos
# max_instances
# min_instances
# delete_policy
# creation_policy


class Config:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            config_dict = json.load(f)
            self.__dict__.update(config_dict)
