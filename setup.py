from setuptools import setup

setup(
    name='University Helper Engine',
    packages=['UHE'],
    include_package_data=True,
    install_requires=[
        'flask','flask_login'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest','flask_login'
    ],
)