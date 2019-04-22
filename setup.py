#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError as excp:
    from distutils.core import setup

import vmrun

setup(	name = 'vmrun',
    version = vmrun.__version__,
    description = 'Control Vmware from Python. Used the vmrun.exe',
    author = 'Binjo',
    author_email = 'binjo.cn@gmail.com',
    url = 'http://github.com/binjo/vmrun-python.git',
    download_url = '',
    license = 'GNU GPL v2',
    keywords = 'vmrun vmware python',
    platforms = ['any'],
    classifiers =	['Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU GPL v2',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering :: VMWare',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    long_description = "\n".join(vmrun.__doc__.split('\n')),
    py_modules = ['vmrun'],
    install_requires = ['setuptools'],
    data_files = [('.', ['README'])] )
