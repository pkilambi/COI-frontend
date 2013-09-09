import yaml

ERROR   = '\033[91m'
OK      = '\033[92m'
WARNING = '\033[93m'
END     = '\033[0m'


def load_yaml(yaml_in_file):
    """
      Load a yaml file and access data
    """
    if not yaml_in_file or not os.path.exists(yaml_in_file):
       return {}
    with open(yaml_in_file, 'r') as f:
        doc = yaml.load(f)
    return doc

def write_yaml(yaml_in_file, data):
    """
     Writes the json to a yaml file
    """
    with open(yaml_in_file, 'a') as yml:
        yaml.dump(data, yml, default_flow_style=False)
    print_ok("Successfully updated yaml file")

def print_warn(text):
    print WARNING + text + END

def print_ok(text):
    print OK + text + END

def print_error(text):
    print ERROR + text + END



