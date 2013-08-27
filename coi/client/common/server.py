# -*- coding: utf-8 -*-
#


import base64
from M2Crypto import SSL, httpslib
try:
    import json
except ImportError:
    import simplejson as json


class BaseConnection(object):

    @classmethod
    def _connection(cls, host, port, protocol, context=None):
        if protocol == 'http':
            return httplib.HTTPConnection(host, port)
        elif protocol == 'https':
            return httpslib.HTTPSConnection(host, port, ssl_context=context)
        else:
            raise Exception("Unknown protocol %s" % protocol)

    def connect(self, host, port, protocol, context=None):
        return _connection(host, port, protocol, context=context)


class SSLConnection(BaseConnection):

    def __init__(self, cert_file, key_file, ca_cert=None):
        super(SSLConnection, self).__init__()
        self.cert_file = cert_file
        self.key_file  = key_file
        self.ca_cert   = ca_cert

    def connect(self, host, port, protocol='https'):
        context = SSL.Context("sslv3")
        if self.cert_file:
            context.load_cert(self.cert_file, keyfile=self.key_file)
        if self.ca_cert:
            context.load_verify_info(self.ca_cert)
        return self._connection(host, port, protocol, ssl_context=context)


class PuppetConnection(object):
    """
     Puppetmaster server connection adaptor
    """
    def __init__(self, host, port=443, handler='/api/', ssl_cert=None,
                       cert_key=None, cert_ca=None):
        self.host      = host
        self.port      = port
        self.handler   = handler
        self.cert_file = ssl_cert
        self.key_file  = cert_key
        self.ca_cert   = cert_ca
        self.headers  = {"Content-type": "application/json",
                         "Accept": "application/json"}

    def _request(self, request_type, method, body=None):
        conn_obj = SSLConnection(self.cert_file, self.key_file, self.ca_cert)
        connection = conn_obj.connect()
        connection.request(request_type, self.handler + method,
                         body=json.dumps(body), headers=self.headers)
        response = conn.getresponse()
        return self._parse_response(response)

    def _parse_response(self, response):
        if response.status not in [200, 202]:
            raise Exception()
        data = response.read()
        if not len(data):
            return None
        return json.loads(data)

    def GET(self, method):
        return self._request("GET", method)

    def POST(self, method, params=""):
        return self._request("POST", method, params)

    def DELETE(self, method, body=None):
        return self._request("DELETE", method, body=body)

    def HEAD(self, method):
        return self._request("HEAD", method)

    def PUT(self, method, body):
        return self._request("PUT", method, body=body)

