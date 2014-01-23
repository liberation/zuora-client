"""
Client for Zuora SOAP API
"""
# TODO:
#  - Handle debug
#  - Handle error
#  - Session policy
import os

from suds.client import Client
from suds.sax.element import Element

from zuora.transport import HttpTransportWithKeepAlive


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
        self.wsdl = wsdl
        self.login = login
        self.password = password

        self.session = None
        self.wsdl_path = 'file://%s' % os.path.abspath(self.wsdl)

        self.client = Client(
            self.wsdl_path,
            transport=HttpTransportWithKeepAlive())

    def instanciate(self, instance_type_string):
        """
        Create object for client.factory.
        """
        return self.client.factory.create(instance_type_string)

    def __str__(self):
        """
        Display the client __str__ method.
        """
        return self.client.__str__()
