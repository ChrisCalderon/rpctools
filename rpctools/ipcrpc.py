"""This module defines an RPC client class that uses an Unix domain
socket to communicate with the go-ethereum client."""
from socket import socket, AF_UNIX, SOCK_STREAM, SHUT_RDWR
import os
from .rpc_client_base import BaseRpcClient


default_address = os.path.join(os.path.expanduser('~'),
                               '.ethereum', 'geth.ipc')  # default path for go-ethereum
RECV_CHUNK = 4096 # max number of bytes to read from connection at a time.


class RpcClient(BaseRpcClient):
    """An RPC client class that uses go-ethereum's 'ipc' interface."""
    def __init__(self, address=default_address, verbose=False):
        BaseRpcClient.__init__(self, verbose)
        self.connection = socket(AF_UNIX, SOCK_STREAM)
        self.connection.connect(address)

    def close(self):
        """Closes the connection."""
        self.connection.shutdown(SHUT_RDWR)
        self.connection.close()

    def _send(self, json):
        """Sends send stringified JSONRPC messages through go-ethereum's Unix Domain socket."""
        self.connection.sendall(json)
        result = bytearray()
        while not self.is_valid_json(result.decode('utf8')):
            result.extend(self.connection.recv(RECV_CHUNK))
        return result
