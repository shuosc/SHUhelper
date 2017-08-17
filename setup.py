
from setuptools import setup,find_packages

setup(
    name='university_helper_engine',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)