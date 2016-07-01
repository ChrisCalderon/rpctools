"""A client for the Etherscan geth proxy API."""
import re
import requests

HEADERS = {'User-Agent': 'pyrpctools',
           'Accept': 'application/json',
           'Accept-Encoding': 'gzip'}
HEX = re.compile('^0x[0-9a-f]+$')


def is_hex(stuff):
    """Predicate that returns true iff `stuff` is a hex string."""
    return isinstance(stuff, str) and HEX.match(stuff.lower())


def is_eth_addr(stuff):
    """Predicate that returns true iff `stuff` looks like an ethereum address."""
    return is_hex(stuff) and len(stuff) == 42


def check_eth_address(stuff):
    """If `stuff` is not an Ethereum address, raises an RpcClientError."""
    if not is_eth_addr(stuff):
        raise RpcClientError('invalid address: {}'.format(stuff))


def is_hash(stuff):
    """Predicate the returns true iff `stuff` looks like a 256 bit, hex encoded digest."""
    return is_hex(stuff) and len(stuff) == 66


def process_tag(tag):
    """Does type checking and/or conversion to hex."""
    if isinstance(tag, str) and tag not in ('latest', 'earliest', 'pending'):
        raise RpcClientError("invalid tag string: {}".format(tag))
    elif isinstance(tag, int):
        tag = hex(tag)
    else:
        raise RpcClientError("invalid tag: <val {}> {}".format(tag, type(tag)))
    return tag


def process_int(n, name):
    """Checks type and converts to hex."""
    if not isinstance(n, (int, long)):
        raise RpcClientError("{} must be an int: {}".format(name, n))
    return hex(n)


class EtherscanRPCError(Exception): pass


class EtherscanRPC(object):
    """An RPC client for the etherscan.io geth proxy API.
    See the documentation at https://etherscan.io/apis#proxy
    """
    def __init__(self, api_key=None):
        """Opens a connection to api.etherscan.io.
        Argument:
        api_key -- An API key from an Etherscan account. Not required,
                   but the connection will be rate limited without it.
        """
        self.address = 'https://api.etherscan.io/api'
        self.common_params = {'module':'proxy'}
        if api_key:
            self.common_params['apikey'] = api_key

    def _dispatcher(self, method, **params):
        # Does an RPC request for the given action and extra parameters.
        params.update(self.common_params)
        return requests.get(url=self.address, params=params, headers=HEADERS).json()

    def eth_blockNumber(self):
        return self._dispatcher('eth_blockNumber')

    def eth_getBlockByNumber(self, tag, boolean=False):
        return self._dispatcher('eth_getBlockByNumber',
                                tag=process_tag(tag),
                                boolean=str(bool(boolean)).lower())

    def eth_getBlockTransactionCountByNumber(self, tag):
            return self._dispatcher('eth_getBlockTransactionCountByNumber',
                                    tag=process_tag(tag))

    def eth_getTransactionByHash(self, txhash):
        if not is_hash(txhash):
            raise RpcClientError('invalid txhash: {}'.format(txhash))
        return self._dispatcher('eth_getTransactionByHash', txhash=txhash)

    def eth_getTransactionByBlockNumberAndIndex(self, tag, index):
        return self._dispatcher('eth_getTransactionByBlockNumberAndIndex',
                                tag=process_tag(tag),
                                index=process_int(index, 'index'))

    def eth_getTransactionCount(self, address, tag):
        check_eth_address(address)
        return self._dispatcher('eth_getTransactionCount',
                                address=address,
                                tag=process_tag(tag))

    def eth_sendRawTransaction(self, tx_hex):
        if not is_hex(tx_hex):
            raise RpcClientError('invalid transaction hex: {}'.format(tx_hex))
        return self._dispatcher('eth_sendRawTransaction',
                                hex=tx_hex)

    def eth_getTransactionReceipt(self, tx_hash):
        if not is_hash(tx_hash):
            raise RpcClientError('invalid transaction hash: {}'.format(tx_hash))
        return self._dispatcher('eth_getTransactionReceipt',
                                txhash=tx_hash)

    def eth_call(self, address, data):
        check_eth_address(address)

        if not is_hex(data):
            raise RpcClientError('`data` must be hex: {}'.format(data))
        
        return self._dispatcher('eth_call',
                                to=address,
                                data=data)

    def eth_getCode(self, address, tag):
        check_eth_address(address)
        return self._dispatcher('eth_getCode',
                                address=address,
                                tag=process_tag(tag))

    def eth_getStorageAt(self, address, position, tag):
        check_eth_address(address)
        return self._dispatcher('eth_getStorageAt',
                                address=address,
                                position=process_int(position, 'position'),
                                tag=process_tag(tag))

    def __getattr__(self, name):
        raise EtherscanRpcError("{} unsupported by Etherscan.".format(name))
