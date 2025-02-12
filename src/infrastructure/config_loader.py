import json
import os


class ConfigLoader:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path

    def load_config(self,configname) :
        # read file in config {configname}.json
        
        configfileabs = os.path.join(self.config_file_path, "{}.json".format(configname))
        
        with open(configfileabs, 'r') as config_file:
            return json.load(config_file)