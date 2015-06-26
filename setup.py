#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reversion_extras'))
from version import __version__

try:
    from setuptools import setup, Command
except ImportError:
    from distutils.core import setup, Command

version = '.'.join(str(x) for x in __version__)

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

requirements = [
    'django-reversion',
]

test_requirements = [
    'pytest',
    'tox'
]

# Add Python 2.7-specific dependencies
if sys.version < '3':
    requirements.append('mock')

# There are no Python 3-specific dependencies to add

long_description = readme + '\n\n' + history

if sys.argv[-1] == 'readme':
    print(long_description)
    sys.exit()


class PyTest(Command):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        self.pytest_args = []

    def finalize_options(self):
        pass

    def run(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='django-reversion-extras',
    version=version,
    description=("""Extra tools to work with django-reversion"""
                 ),
    long_description=long_description,
    author='Fabio C. Barrionuevo da Luz',
    author_email='bnafta@gmail.com',
    url='https://github.com/luzfcb/django-reversion-extras',
    packages=[
        'reversion_extras',
    ],
    package_dir={'reversion_extras': 'reversion_extras'},
    include_package_data=True,
    install_requires=requirements,
    license='BSD',
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Environment :: Django',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',

    ],
    keywords=(
        'django-reversion, reversion, reversion-extras'
    ),
    cmdclass={'test': PyTest},
    test_suite='tests',
    tests_require=test_requirements
)
