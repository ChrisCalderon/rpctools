"""A JSONRPC class with an IPC backend."""
from socket import socket, AF_UNIX, SOCK_STREAM, SHUT_RDWR
from rpctools.jsonrpc import JSONRPC, is_valid_json

RECV_CHUNK = 4096  # max number of bytes to read from connection at a time.


class IPCRPC(JSONRPC):
    """Sends JSON RPC over an Unix domain socket."""
    def __init__(self, address, verbose):
        """Create a connection for JSONRPC to `address`.

        Arguments:
        address -- The path to the Unix domain socket of an Ethereum
        client. This is a file path, not a url!
        verbose -- Tells whether or not to print messages.
        """
        JSONRPC.__init__(self, verbose)
        self.connection = socket(AF_UNIX, SOCK_STREAM)
        self.connection.connect(address)

    def close(self):
        """Closes the connection."""
        self.connection.shutdown(SHUT_RDWR)
        self.connection.close()

    def _send(self, json):
        # Sends stringified JSONRPC messages through  Unix Domain socket.
        self.connection.sendall(json)
        result = bytearray()
        while not is_valid_json(result.decode('utf8')):
            result.extend(self.connection.recv(RECV_CHUNK))
        return result
