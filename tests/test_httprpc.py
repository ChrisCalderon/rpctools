from BaseTestClass import BaseTest
from rpctools import HTTPRPCClient

class TestHTTPRPC(BaseTest):
    def make_rpc_client(self):
        return HTTPRPCClient()
