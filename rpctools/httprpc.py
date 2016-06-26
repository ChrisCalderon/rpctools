from rpctools.rpc_client_base import BaseRpcClient
import httplib

REQUEST_HEADERS = {'User-Agent': 'dapper/1.0',
                   'Content-Type': 'application/json',
                   'Accept': 'application/json'}
default_address = ('localhost', 8545)  # the go-ethereum default address


class RpcClient(BaseRpcClient):
    def __init__(self, address=default_address, verbose=False):
        BaseRpcClient.__init__(self, verbose)
        self.connection = httplib.HTTPConnection(*address)
        if address[0] in ('localhost', '127.0.0.1'):
            self.is_local = True
        else:
            self.is_local = False

    def close(self):
        self.connection.close()

    def _send(self, json):
        self.connection.request('POST', '/', json,
                                REQUEST_HEADERS)

        response = self.connection.getresponse()
        return response.read()
