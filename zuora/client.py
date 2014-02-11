"""
Client for Zuora SOAP API
"""
import os
import logging
from datetime import datetime
from datetime import timedelta
from ConfigParser import SafeConfigParser

from suds import WebFault
from suds.client import Client
from suds.sax.text import Text
from suds.sax.element import Element

from zuora.transport import HttpTransportWithKeepAlive

DEFAULT_SESSION_DURATION = 15 * 60

logger = logging.getLogger(__name__)
logger_suds = logging.getLogger('suds')
logger_suds.propagate = False


class ZuoraException(Exception):
    """
    Base Zuora Exception.
    """
    pass


class BaseZuora(object):
    """
    SOAP Client based on Suds
    """

    def __init__(self, wsdl, username, password,
                 session_duration=DEFAULT_SESSION_DURATION):
        self.wsdl = wsdl
        self.username = username
        self.password = password

        self.session = None
        self.session_duration = session_duration
        self.session_expiration = datetime.now()
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
        self.session_expiration = datetime.now() + timedelta(
            seconds=self.session_duration)
        session_namespace = ('ns1', 'http://api.zuora.com/')
        session = Element('session', ns=session_namespace).setText(session_id)
        header = Element('SessionHeader', ns=session_namespace)
        header.append(session)
        self.client.set_options(soapheaders=[header])

    def reset(self):
        """
        Reset the connection to the API.
        """
        self.session = None
        self.client.options.transport = HttpTransportWithKeepAlive()

    def call(self, method, *args, **kwargs):
        """
        Call a SOAP method.
        """
        if self.session is None or self.session_expiration >= datetime.now():
            self.login()

        try:
            response = method(*args, **kwargs)
            logger.info('Sent: %s', self.client.last_sent())
            logger.info('Received: %s', self.client.last_received())
            if isinstance(response, Text):  # Occasionally happens
                logger.warning('Invalid response %s, retrying...', response)
                self.reset()
                return self.call(method, *args, **kwargs)
        except WebFault as error:
            if error.fault.faultcode == 'fns:INVALID_SESSION':
                logger.warning('Invalid session, relogging...')
                self.reset()
                return self.call(method, *args, **kwargs)
            else:
                logger.info('Sent: %s', self.client.last_sent())
                logger.info('Received: %s', self.client.last_received())
                logger.error('WebFault: %s', error.__dict__)
                raise ZuoraException('WebFault: %s' % error.__dict__)
        except Exception as error:
            logger.info('Sent: %s', self.client.last_sent())
            logger.info('Received: %s', self.client.last_received())
            logger.error('Unexpected error: %s', error)
            raise ZuoraException('Unexpected error: %s' % error)

        logger.debug('Successful response %s', response)
        return response

    def amend(self, amend_requests):
        """
        Amend susbcriptions.
        """
        response = self.call(
            self.client.service.amend,
            amend_requests)
        return response

    def create(self, z_objects):
        """
        Create z_objects.
        """
        response = self.call(
            self.client.service.create,
            z_objects)
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

    def generate(self, z_objects):
        """
        Generate z_objects.
        """
        response = self.call(
            self.client.service.execute,
            z_objects)
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
        response = self.client.service.login(self.username, self.password)
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

    def subscribe(self, subscribe_requests):
        """
        Subscribe accounts.
        """
        response = self.call(
            self.client.service.subscribe,
            subscribe_requests)
        return response

    def update(self, z_objects):
        """
        Update z_objects.
        """
        response = self.call(
            self.client.service.update,
            z_objects)
        return response

    def __str__(self):
        """
        Display the client __str__ method.
        """
        return self.client.__str__()


class Zuora(BaseZuora):
    """
    Final SOAP Zuora Client
    """

    def __init__(self):
        default_config = {'session_duration': str(DEFAULT_SESSION_DURATION)}

        config = SafeConfigParser(default_config)
        config.add_section('client')
        config.read([os.path.expanduser('~/.zuora.cfg'),
                     os.path.join(os.getcwd(), 'etc/zuora.cfg')])

        wsdl = config.get('client', 'wsdl')
        username = config.get('client', 'username')
        password = config.get('client', 'password')
        session_duration = config.getint('client', 'session_duration')

        super(Zuora, self).__init__(
            wsdl, username, password, session_duration)
