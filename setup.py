#!/usr/bin/env python

import setuptools

from pbr.packaging import parse_requirements

entry_points = {
    'openstack.cli.extension': [
        'outage = langstrothclient.osc.plugin'],
    'openstack.outage.v1': [
        'outage list = langstrothclient.osc.v1.outages:ListOutages',
        'outage show = langstrothclient.osc.v1.outages:ShowOutage']
}

setuptools.setup(
    name='langstrothclient',
    version='0.2.0',
    description='Client for the Nectar Status and Outage system (Langstroth)',
    author='Stephen Crawley',
    author_email='stephen.crawley@ardc.edu.au',
    url='https://github.com/NeCTAR-RC/python-langstrothclient',
    packages=['langstrothclient'],
    install_requires=parse_requirements(),
    include_package_data=True,
    setup_requires=['pbr>=3.0.0'],
    license='Apache',
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'],
    entry_points=entry_points,
)
