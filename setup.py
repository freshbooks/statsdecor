#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


readme = open('README.md').read()
requirements = open('requirements.txt').readlines()
VERSION = open('VERSION').read().strip()

setup(
    name='statsdecor',
    version=VERSION,
    description='A set of decorators and helper methods '
                'for adding statsd metrics to applications.',
    long_description=readme + '\n\n',
    long_description_content_type='text/markdown',
    author='Freshbooks Dev Team',
    author_email='opensource@freshbooks.com',
    url='https://github.com/freshbooks/statsdecor',
    packages=find_packages(exclude=['test*']),
    include_package_data=True,
    install_requires=requirements,
    license="MIT",
    zip_safe=False,
    keywords='statsd, stats',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    test_suite='tests'
)
