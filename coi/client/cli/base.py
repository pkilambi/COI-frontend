#!/usr/bin/python
import os
import yaml
import copy
import pprint
import messages
from StringIO import StringIO
from clint.textui import colored

class InstallerError(Exception):
    """
    Installer Exception wrapper
    """
    def __init__(self, message, exception):
        super(InstallerError, self).__init__(message, exception)
        self.message = message
        self.exception = exception

    def __str__(self):
        return repr(self.message) + ": " + repr(self.exception)


class BaseConfig(object):
    """Base Installer class."""

    params = []
    message = None

    def __init__(self, yaml_in_file=None):
        self.yaml_in_file = yaml_in_file

    def askme(self, question, suggestions=None, default=None):
        """
         Prompt the questions for user input
        """
        while True:
            msg = StringIO()
            msg.write(question)
            msg.seek(0)

            answer = raw_input(msg.read() + "[%s]" % default + ": ")
            if not len(answer):
                if default:
                    answer = default
                else:
                    msg.close()
                    continue
            if suggestions and (answer not in suggestions):
                print(colored.red("Invalid choice, please pick a valid option from the following %s" % suggestions))
                msg.close()
                continue
	    return answer

    def setup(self):
        """
         Setup method that does the real work of loading the yaml,
         generating questions, parsing the output and writing to
         a yaml file.
        """
        if not os.path.exists(self.yaml_in_file):
            return {}
        print(colored.green(messages.INSTALLER_HEADER))
        print(colored.green(self.message))
        doc = self.load_yaml()
        doc_copy = copy.deepcopy(doc)
        for key in doc_copy.keys():
            param = [i for i in self.params if key == i['key']]
            if not param:
                continue
            param = param[0]
            ans = self.askme(param['prompt'],
                             suggestions=param['options'],
                             default=param['default'])
            if ans:
                doc_copy[key] = ans
        pprint.pprint(doc_copy)

    def load_yaml(self):
        """
         Load a yaml file and access data
        """
        with open(self.yaml_in_file, 'r') as f:
            doc = yaml.load(f)
        return doc

    def write_yaml(self, data, yaml_out_file):
        """
         Writes the json to a yaml file
        """
        with open(yaml_out_file, 'w') as yml:
            yaml.dump(data, yml, allow_unicode=True)


class GlobalConfig(BaseConfig):

    params = [{"prompt"  : "Please specify the domain name",
               "key"     : "domain",
               "options" : None,
               "default" : "domain.name"},
              {"prompt"  : "What Operating System would you like to use",
               "key"     : "operatingsystem",
               "options" : ["redhat", "ubuntu"],
               "default" : "redhat"},
              {"prompt"  : "What Scenario would you like to setup",
               "key"     : "scenario",
               "options" : ["multinode", "allinone", "multinode-ha"],
               "default" : "allinone"},
              {"prompt"  : "List of NTP Servers to use",
               "key"     : "ntp_server",
               "options" : None,
               "default" : None,},]
    message = "Global Configuration"

    def __init__(self, yaml_in_file='config.yaml'):
        super(GlobalConfig, self).__init__(yaml_in_file)


def setup_installer():
    global_config = GlobalConfig()
    global_config.setup()


if __name__ == '__main__':
    setup_installer()
