#!/usr/bin/env python

from __future__ import print_function
from setuptools import setup
import ast

package_name = 'set-signatures'
filename = package_name + '.py'

def get_version():
    with open(filename) as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s

setup(
    name=package_name,
    version=get_version(),
    description='Allows G Suite administrators to change email signatures en masse using a convenient mustache template.',
    url='https://github.com/eberkund/gsuite-signature-manager',
    py_modules=[package_name],
    entry_points={
        'console_scripts': [
            'set-signatures = set-signatures:__main__'
        ]
    },
)
