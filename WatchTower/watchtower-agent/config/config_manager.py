import yaml

class ConfigManager:
    def __init__(self, config_path='config/default_config.yaml') -> None:
        self.config_path = config_path
        self.config = self.load_config()

    def load_config(self) -> yaml:
        with open(self.config_path, 'r') as file:
            return yaml.safe_load(file)

    def get(self, key, default=None):
        return self.config.get(key, default)