# modules/config_loader.py
import yaml

class ConfigLoader:
    def __init__(self, config_path='config/conf.yaml', projects_path='config/projects.yaml'):
        self.config = self.load_yaml(config_path)
        self.projects = self.load_yaml(projects_path)

    def load_yaml(self, path):
        try:
            with open(path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Configuration file {path} not found.")
            return {}
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file {path}: {e}")
            return {}
