"""
Client for Zuora SOAP API
"""
# TODO:
#  - Handle debug
#  - Handle error
#  - Session policy
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

    def __str__(self):
        return self.client.__str__()
