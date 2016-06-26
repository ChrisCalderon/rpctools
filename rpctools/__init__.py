from rpctools.rpc_client_base import RPCClientError
from rpctools.httprpc import RpcClient as HTTPRPCClient
from rpctools.ipcrpc import RpcClient as IPCRPCClient
import os as _os
import stat as _stat
import re as _re

_HTTP_HOST = _re.compile('^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|[\w\.]+)$')


def _is_uds_path(address):
    try:
        return _os.path.is_file(address) and _stat.S_ISSOCK(_os.stat(address).st_mode)
    except:
        return False


def _is_http_address(address):
    return (isinstance(address, tuple) and
            len(address)==2 and
            isinstance(address[0], str) and
            isinstance(address[1], int) and
            _HTTP_HOST.match(address[0]) and
            0<address[1]<65536)


def rpc_client_factory(address):
    if _is_uds_path(address):
        return IPCRPCClient(address)
    elif _is_http_address(address):
        return HTTPRPCClient(address)
    else:
        raise RPCClientError("Bad address format: Not ipc path or ('host', port) tuple.")
