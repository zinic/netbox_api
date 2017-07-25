#!/usr/bin/env python
from setuptools import setup, find_packages

# Installation requirements needed absolutely for the program to run
install_requires = [
    'tabulate>=0.7.7',
    'requests>=2.18.1'
]

# Additional feature sets and their requirements
extras_require = {
}

setup(
    name='netbox_api',
    version='0.4.1',
    description="""Netbox API bindings and tools for Python
    Website: https://github.com/zinic/netbox_api
    """,
    author='John Hopper',
    author_email='john.hopper@jpserver.net',
    packages=find_packages(),

    install_requires=install_requires,
    extras_require=extras_require,

    entry_points={
        'console_scripts': [
            'netbox_api=netbox_api:main',
        ],
    }
)
