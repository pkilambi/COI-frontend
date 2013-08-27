#!/usr/bin/env python

"""
distutils/setuptools install script.
"""

from setuptools import setup, find_packages

packages = [
    "coi",
    "coi.client",
    "coi.client.api",
    "coi.client.cli",
]

requires = (
    "iniparse",
    "simplejson",
    "M2Crypto"
)


setup(
    name        = 'COI-frontend',
    version     = "0.1",
    description = "Frontend framework for Cisco Openstack Installer ",
    url         = 'http://github.com/pkilambi/COI-frontend',
    license     ='GPLv2+',
    author      ='Pradeep Kilambi',
    author_email='pkilambi@cisco.com',
    packages    = packages,
    package_dir = { "coi" : "coi" },
    scripts     = ['bin/coi-installer'],
    requires    = requires
)

