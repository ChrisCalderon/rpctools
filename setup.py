from setuptools import setup

with open('requirements.txt') as reqs:
    requirements = filter(lambda r: r!='',
                          map(lambda r: r.strip(),
                              reqs))

setup(name='PyRPCTools',
      version='1.0',
      description='JSONRPC Classes for Ethereum Nodes.',
      author='ChrisCalderon',
      author_email='calderon.christian760@gmail.com',
      packages=['rpctools'],
      install_requires=requirements)
