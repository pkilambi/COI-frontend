#!/usr/bin/python
import os
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

    def __init__(self, yaml_in_file="config.yaml"):
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
        doc = self.execute_params(self.params)
        return doc

    def execute_params(self, params):
        doc = {}
        for param in params:
            ans = self.askme(param['prompt'],
                             suggestions=param['options'],
                             default=param['default'])
            if ans:
                doc[param['key']] = ans
        return doc


class HeaderConfig(BaseConfig):

    params = []
    message = messages.INSTALLER_HEADER

    def __init__(self, yaml_in_file=None):
        super(HeaderConfig, self).__init__(yaml_in_file)


class GlobalConfig(BaseConfig):

    params = [
              {"prompt"  : "Please specify the domain name",
               "key"     : "domain",
               "options" : None,
               "default" : "domain.name"},
              {"prompt"  : "What Operating System would you like to use",
               "key"     : "operatingsystem",
               "options" : ["redhat", "ubuntu"],
               "default" : "redhat"},
              {"prompt"  : "What Role would you like to setup",
               "key"     : "role",
               "options" : ["openstack",],
               "default" : "openstack"},
              {"prompt"  : "What Scenario would you like to setup",
               "key"     : "scenario",
               "options" : ["multinode", "allinone", "multinode-ha"],
               "default" : "allinone"},
               {"prompt"  : "List of NTP Servers to use",
               "key"     : "ntp_server",
               "options" : None,
               "default" : "clock.redhat.com",},
              {"prompt"  : "Verbose",
               "key"     : "verbose",
               "options" : ['y', 'n'],
               "default" : 'n',},]

    apt_params = [
              {"prompt" : "Would you like to setup apt mirror",
               "key"    : "apt_mirror",
               "options": [],
               "default": "us.archive.ubuntu.com"},
              {"prompt" : "Would you like to setup apt cache",
               "key"    : "apt_cache",
               "options": [],
               "default": "192.168.242.99"}, ]

    message = "Global Configuration"

    def __init__(self, yaml_in_file='config.yaml'):
        super(GlobalConfig, self).__init__(yaml_in_file)

    def setup(self):
        doc = {}
        utils.print_ok(self.message)
        _basic_params = self.execute_params(self.params)
        doc.update(_basic_params)
        if _basic_params['operatingsystem'] == 'ubuntu':
            _apt_params = self.execute_params(self.apt_params)
            doc.update(_apt_params)
        elif _basic_params['operatingsystem'] == 'redhat':
            #do redhat specific options if any
            pass
        return doc


class OpenstackConfig(BaseConfig):

    params  = [
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
              {"prompt"  : "What network service should we use?",
               "key"     : "network_service",
               "options" : ['neutron', 'nova'],
               "default" : 'neutron',}]

    message = "Openstack Configuration"

    def __init__(self, yaml_in_file='config.yaml'):
        super(OpenstackConfig, self).__init__(yaml_in_file)


class NeutronConfig(OpenstackConfig):

    params = [
              {"prompt"  : "What type of network plugin should we use?",
               "key"     : "network_plugin",
               "options" : ['ovs', 'linuxbridge', 'cisco'],
               "default" : 'ovs',},
              {"prompt"  : "What network type should we use?",
               "key"     : "network_type",
               "options" : ['single-flat', 'provider-router', 'per-tenant-router'],
               "default" : 'per-tenant-router',},
              {"prompt"  : "What tenant network type should we use?",
               "key"     : "tenant_network_type",
               "options" : ['gre', 'vlan'],
               "default" : 'gre'},
               ]

    message = "Neutron Configuration"

    def __init__(self, yaml_in_file='config.yaml'):
        super(NeutronConfig, self).__init__(yaml_in_file)
   

class CinderConfig(OpenstackConfig):

    params = [
              {"prompt"  : "backend for cinder?",
               "key"     : "cinder_backend",
               "options" : ['iscsi',],
               "default" : 'iscsi',},]

    message = "Cinder Configuration"

    def __init__(self, yaml_in_file='config.yaml'):
        super(CinderConfig, self).__init__(yaml_in_file)

 
def setup_installer():
    data = {}
    for cls in [HeaderConfig, GlobalConfig,]:
        config = cls()
        doc = config.setup()
        if doc: 
            data.update(doc)
    _ostack_params = OpenstackConfig().setup()
    data.update(_ostack_params)
    if data['network_service'] == 'neutron':
        _neutron_params = NeutronConfig().setup()
        data.update(_neutron_params)
    if data['enable_cinder'] == 'y':
        _cinder_params = CinderConfig().setup()
        data.update(_cinder_params)    
    yaml_obj = utils.YamlParser()
    yaml_obj.write_yaml(data)

if __name__ == '__main__':
    setup_installer()
