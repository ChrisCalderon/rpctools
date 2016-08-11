"""A class for JSONRPC over HTTP or HTTPS."""
from rpctools.jsonrpc import JSONRPC
import requests

HEADERS = {'User-Agent': 'rpctools/{}',
           'Content-Type': 'application/json',
           'Accept': 'application/json'}


class HTTPRPC(JSONRPC):
    """Sends JSON RPC through an HTTP or HTTPS backend."""
    def __init__(self, address, verbose):
        """Uses an address to connect to an Ethereum node.

        Arguments:
        address -- A browser-style address, like 'http://mydomain.com:port'.
        This class can use http or https and can be used for local nodes or
        public ones.
        verbose -- If True, prints each message.
        """
        JSONRPC.__init__(self, verbose)
        self.address = address

    def _send(self, json):
        r = requests.post(url=self.address, data=json, headers=HEADERS)
        return r.content
