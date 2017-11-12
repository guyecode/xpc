from setuptools import setup

VERSION = '0.1.0'

setup(
    name='xpc',
    description='xpc web server',
    version=VERSION,
    packages=['web'],
    install_requires=[
        "tornado==4.2.1",
        "simplejson==3.8.0"
    ])
