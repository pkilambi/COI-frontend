#!/usr/bin/python
import os
import yaml
import copy
import pprint
import messages
from StringIO import StringIO
from coi.client.common import utils

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
                if default is not None:
                    answer = default
                else:
                    msg.close()
                    continue
            if suggestions and (answer not in suggestions):
                utils.print_error("Invalid choice, please pick a valid option from the following %s" % suggestions)
                msg.close()
                continue
	    return answer

    def setup(self):
        """
         Setup method that does the real work of loading the yaml,
         generating questions, parsing the output and writing to
         a yaml file.
        """
        utils.print_ok(self.message)
        doc = self.load_yaml()
        for key, value in doc.items():
            param = [i for i in self.params if key == i['key']]
            if not param:
                continue
            param = param[0]
            ans = self.askme(param['prompt'],
                             suggestions=param['options'],
                             default=param['default'])
            if ans:
                doc[key] = ans
        #pprint.pprint(doc)
        self.write_yaml(doc)
    
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
        if not self.yaml_in_file or not os.path.exists(self.yaml_in_file):
            return {}
        with open(self.yaml_in_file, 'w') as yml:
            yaml.dump(data, yml, default_flow_style=False)
        utils.print_ok("Successfully updated yaml file")


class HeaderConfig(BaseConfig):

    params = []
    message = messages.INSTALLER_HEADER

    def __init__(self, yaml_in_file=None):
        super(HeaderConfig, self).__init__(yaml_in_file)

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
               "default" : None,},
              {"prompt"  : "Verbose",
               "key"     : "verbose",
               "options" : None,
               "default" : False,},
              {"prompt"  : "What type of database you like to use?",
               "key"     : "db_type",
               "options" : ['mysql', 'postgres'],
               "default" : 'mysql',},
              {"prompt"  : "What rpc service type you like to use?",
               "key"     : "rpc_type",
               "options" : ['qpid', 'rabbitmq'],
               "default" : 'rabbitmq',},
              {"prompt"  : "Enable nova service?",
               "key"     : "enable_nova",
               "options" : ['y', 'n'],
               "default" : 'y',},
              {"prompt"  : "Enable network service?",
               "key"     : "enable_network",
               "options" : ['y', 'n'],
               "default" : 'y',},
              {"prompt"  : "Enable keystone service?",
               "key"     : "enable_keystone",
               "options" : ['y', 'n'],
               "default" : 'y',},
              {"prompt"  : "Enable glance service?",
               "key"     : "enable_glance",
               "options" : ['y', 'n'],
               "default" : 'y',},
              {"prompt"  : "Enable swift service?",
               "key"     : "enable_swift",
               "options" : ['y', 'n'],
               "default" : 'y',},
              {"prompt"  : "Enable cinder service?",
               "key"     : "enable_cinder",
               "options" : ['y', 'n'],
               "default" : 'y',},
              {"prompt"  : "Enable ceph service?",
               "key"     : "enable_ceph",
               "options" : ['y', 'n'],
               "default" : 'y',},
              {"prompt"  : "backend for cinder?",
               "key"     : "cinder_backend",
               "options" : ['iscsi',],
               "default" : 'iscsi',},
              {"prompt"  : "What type of networking should we use?",
               "key"     : "network_type",
               "options" : ['neutron', 'nova'],
               "default" : 'neutron',},]


    message = "Global Configuration"

    def __init__(self, yaml_in_file='config.yaml'):
        super(GlobalConfig, self).__init__(yaml_in_file)


def setup_installer():
    for cls in [HeaderConfig, GlobalConfig]:
        config = cls()
        config.setup()


if __name__ == '__main__':
    setup_installer()
