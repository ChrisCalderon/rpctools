from __future__ import print_function
from setuptools import setup
import os
import sys

if sys.version_info >= (3, 0):
    from functools import reduce


class SetupError(Exception):
    pass


def is_http(req):
    """Checks if a requirement is a link."""
    return req.startswith('http://') or req.startswith('https://')


def split_requirements(links_requirements, req):
    """Keeps track of requirements that aren't on PyPI."""
    links, requirements = links_requirements
    if is_http(req):
        i = req.find('#egg')
        if i == -1:
            raise SetupError('Missing \'#egg=\' in requirement link.')
        links.append(req[:i])
        requirements.append(req[i+5:])
    else:
        requirements.append(req)
    return links, requirements


def read_metadata():
    """Finds the package to install and returns it's metadata."""
    subdirs = next(os.walk(os.getcwd()))[1]

    for subdir in subdirs:
        if '__init__.py' in os.listdir(subdir):
            print('Found package:', subdir)
            break
    else:
        raise SetupError('Can\'t find an __init__.py file!')

    metadata = {'name': subdir, 'packages': [subdir]}
    relevant_keys = {'__version__': 'version',
                     '__author__': 'author',
                     '__email__': 'author_email',
                     '__license__': 'license'}

    with open(os.path.join(subdir, '__init__.py')) as m:
        first_line = next(m)
        metadata['description'] = first_line.strip(). strip('\n "')
        for line in m:
            if len(relevant_keys) == 0:
                break
            for key in relevant_keys:
                if line.startswith(key):
                    break
            else:
                continue

            metadatum_name = relevant_keys.pop(key)
            metadata[metadatum_name] = line.split('=', 1)[1].strip('\n\' ')

    if relevant_keys:
        print('FYI; You didn\'t put the following info in your __init__.py:')
        print('   ', ', '.join(relevant_keys))

    return metadata

with open('requirements.txt') as reqs:
    links, requirements = reduce(split_requirements,
                                 filter(None, map(str.strip, reqs)),
                                 [[], []])

metadata = read_metadata()
metadata['dependency_links'] = links
metadata['install_requires'] = requirements

setup(**metadata)
