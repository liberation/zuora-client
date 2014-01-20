"""
Client for Zuora SOAP API
"""
# TODO:
#  - Handle debug
#  - Handle error
#  - Session policy
from suds.client import Client
from suds.sax.element import Element


class ZuoraException(Exception):
    """
    Base Zuora Exception.
    """
    pass


class Zuora(object):
    """
    SOAP Client based on Suds
    """

    def __init__(self, wsdl, login, password):
        pass
