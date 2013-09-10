#! /usr/bin/python
import sys
import yaml

ERROR   = '\033[91m'
OK      = '\033[92m'
WARNING = '\033[93m'
END     = '\033[0m'


class YamlParser(object):

    def __init__(self, yaml_in_file="config.yaml"):
        self.yaml_in_file = yaml_in_file

    def load_yaml(self):
        """
         Load a yaml file and access data
        """
        if not self.yaml_in_file or not os.path.exists(self.yaml_in_file):
            return {}
        with open(self.yaml_in_file, 'r') as f:
            doc = yaml.load(f)
        return doc

    def write_yaml(self, data):
        """
         Writes the json to a yaml file
        """
        if self.yaml_in_file is None:
            # nowhere to save
            return
        with open(self.yaml_in_file, 'w') as yml:
            yaml.dump(data, yml, default_flow_style=False)
        print_ok("Successfully updated yaml file")


def print_warn(text):
    print WARNING + text + END

def print_ok(text):
    print OK + text + END

def print_error(text):
    print ERROR + text + END

def system_exit(code, msg=None):
    """
    Helper method to exist with error code and a message
    """
    if msg:
        sys.stderr.write(str(msg) + '\n')
    sys.exit(code)

