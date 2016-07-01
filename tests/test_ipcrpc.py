from rpctools import IpcRpcClient
from BaseTestClass import BaseTest

class TestIPCRPC(BaseTest):
    def make_rpc_client(self):
        return IpcRpcClient()
