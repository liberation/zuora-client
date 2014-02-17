"""
Setup script for Zuora-client
"""
from setuptools import setup
from setuptools import find_packages

import zuora

setup(
    name='zuora-client',
    version=zuora.__version__,

    description='Zuora client SOAP API',
    long_description=open('README.rst').read(),
    keywords='zuora, client, soap, api',

    author=zuora.__author__,
    author_email=zuora.__email__,
    url=zuora.__url__,

    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules'],

    license=zuora.__license__,
    zip_safe=False,
    install_requires=['suds>=0.4',
                      'httplib2>=0.8']
)
