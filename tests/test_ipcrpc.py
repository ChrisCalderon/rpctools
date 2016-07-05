from rpctools import rpc_factory
from BaseTestClass import BaseTest
import os


class TestIPCRPC(BaseTest):
    def make_rpc_client(self):
        return rpc_factory(os.path.join(os.environ['HOME'],
                                        '.parity',
                                        'jsonrpc.ipc'),
                           False)
