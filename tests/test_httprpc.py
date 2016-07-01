from BaseTestClass import BaseTest
from rpctools import HttpRpcClient

class TestHTTPRPC(BaseTest):
    def make_rpc_client(self):
        return HttpRpcClient()
