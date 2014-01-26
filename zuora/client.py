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

    def call(self, method, *args, **kwargs):
        """
        Call a SOAP method.
        """
        return method(*args, **kwargs)

    def login(self):
        """
        Login on the API to get a session.
        """
        response = self.client.service.login(self.login, self.password)
        self.set_session(response.Session)
        return response

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

# amend(AmendRequest[] requests, )
# create(ns2:zObject[] zObjects, )
# delete(xs:string type, ID[] ids, )
# execute(xs:string type, xs:boolean synchronous, ID[] ids, )
# generate(ns2:zObject[] zObjects, )
# getUserInfo()
# login(xs:string username, xs:string password, )
# query(xs:string queryString, )
# queryMore(QueryLocator queryLocator, )
# subscribe(SubscribeRequest[] subscribes, )
# update(ns2:zObject[] zObjects, )
