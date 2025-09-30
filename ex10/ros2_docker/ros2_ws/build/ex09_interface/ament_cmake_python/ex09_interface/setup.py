from setuptools import find_packages
from setuptools import setup

setup(
    name='ex09_interface',
    version='0.0.0',
    packages=find_packages(
        include=('ex09_interface', 'ex09_interface.*')),
)
