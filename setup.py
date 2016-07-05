from setuptools import setup

with open('requirements.txt') as reqs:
    requirements = filter(None, [r.strip() for r in reqs])

setup(name='PyRPCTools',
      version='1.0dev1',
      description='JSON RPC Classes for Ethereum Nodes.',
      author='ChrisCalderon',
      author_email='pythonwiz@protonmail.com',
      packages=['rpctools'],
      install_requires=requirements)
