"""RPC client classes for Ethereum nodes."""
from rpctools.jsonrpc import RPCError
from rpctools.ipcrpc import IPCRPC
from rpctools.httprpc import HTTPRPC
from rpctools.etherscan import EtherscanRPC
import rpctools.httprpc
import os as _os
import re as _re
import stat as _stat

__all__ = ['RPCError', 'IPCRPC', 'HTTPRPC', 'EtherscanRPC', 'rpc_factory']
__version__ = '1.0rc5'
__author__ = 'Chris Calderon'
__license__ = 'MIT'
__email__ = 'pythonwiz@protonmail.com'


_HTTP = _re.compile('^https?://.+(:\d{2,5})?$')
http_user_agent = rpctools.httprpc.HEADERS['User-Agent']
rpctools.httprpc.HEADERS['User-Agent'] = http_user_agent.format(__version__)


def rpc_factory(address, verbose):
    """Chooses the appropriate rpc class based on the address format.

    Does not work for EtherscanRPC because there is no good way to
    check if an api_key is valid. If you know you have an apikey for
    Etherscan, instantiate the EtherscanRPC client directly.
    """
    if not isinstance(address, str):
        raise RPCError('The address must be a string: {!r}'.format(address))

    if _os.path.exists(address) and _stat.S_ISSOCK(_os.stat(address).st_mode):
        return IPCRPC(address, verbose)
    elif _HTTP.match(address):
        return HTTPRPC(address, verbose)
    else:
        raise RPCError('Can\'t match address format to an RPC class.')
