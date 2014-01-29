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

    def set_session(self, session_id):
        """
        Record the session info.
        """
        self.session = session_id
        session_namespace = ('ns1', 'http://api.zuora.com/')
        session = Element('session', ns=session_namespace).setText(session_id)
        header = Element('SessionHeader', ns=session_namespace)
        header.append(session)
        self.client.set_options(soapheaders=[header])

    def call(self, method, *args, **kwargs):
        """
        Call a SOAP method.
        """
        return method(*args, **kwargs)

    def amend(self, *amend_requests):
        """
        Amend susbcriptions.
        """
        response = self.call(
            self.client.service.amend,
            *amend_requests)
        return response

    def create(self, *z_objects):
        """
        Create z_objects.
        """
        response = self.call(
            self.client.service.create,
            *z_objects)
        return response

    def delete(self, object_string, ids=[]):
        """
        Delete z_objects by ID.
        """
        response = self.call(
            self.client.service.delete,
            object_string, ids)
        return response

    def execute(self, object_string, synchronous=False, ids=[]):
        """
        Execute a process by IDs.
        """
        response = self.call(
            self.client.service.execute,
            object_string, synchronous, ids)
        return response

    def generate(self, *z_objects):
        """
        Generate z_objects.
        """
        response = self.call(
            self.client.service.execute,
            *z_objects)
        return response

    def get_user_info(self):
        """
        Return current user's info.
        """
        response = self.call(
            self.client.service.get_user_info)
        return response

    def login(self):
        """
        Login on the API to get a session.
        """
        response = self.client.service.login(self.login, self.password)
        self.set_session(response.Session)
        return response

    def query(self, query_string):
        """
        Execute a query.
        """
        response = self.call(
            self.client.service.query,
            query_string)
        return response

    def query_more(self, query_locator):
        """
        Execute the suite of a query.
        """
        response = self.call(
            self.client.service.queryMore,
            query_locator)
        return response

    def subscribe(self, *subscribe_requests):
        """
        Subscribe accounts.
        """
        response = self.call(
            self.client.service.subscribe,
            *subscribe_requests)
        return response

    def update(self, *z_objects):
        """
        Update z_objects.
        """
        response = self.call(
            self.client.service.update,
            *z_objects)
        return response

    def __str__(self):
        """
        Display the client __str__ method.
        """
        return self.client.__str__()

