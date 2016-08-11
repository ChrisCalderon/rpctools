"""A client for the Etherscan geth proxy API."""
from __future__ import print_function
import requests
from rpctools.httprpc import HEADERS
from rpctools.jsonrpc import RPCError


class EtherscanRPCError(Exception):
    pass


class EtherscanRPC(object):
    """An RPC client for the etherscan.io geth proxy API.

    Notes:
    All hex arguments should start with '0x'.
    Several methods have a tag argument, see the Ethereum docs. [1]
    Also, check out the Etherscan docs! [2]

    [1] https://github.com/ethereum/wiki/wiki/JSON-RPC#the-default-block-parameter
    [2] https://etherscan.io/apis#proxy
    """
    address = 'https://api.etherscan.io/api'
    error = {"status": "0", "message": "NOTOK", "result": "Error!"}
    error_fmt = 'Etherscan doesn\' like your params: {}'

    def __init__(self, api_key, verbose):
        """Opens a connection to api.etherscan.io.

        Argument:
        api_key -- An API key from an Etherscan account.
        verbose -- Optionally print JSON messages. Useful for debugging.
        """
        self.common_params = {'module': 'proxy'}
        self.verbose = verbose
        self.common_params['apikey'] = api_key

    def _dispatch(self, **params):
        # Does an RPC request for the given action and extra parameters.
        params.update(self.common_params)
        r = requests.get(url=self.address, params=params, headers=HEADERS)
        json = r.json()
        if json == self.error:  # The Etherscan API doesn't like your request.
            raise EtherscanRPCError(self.error_fmt.format(params))
        if 'error' in json:
            raise RPCError(json)
        if self.verbose:
            print("Sent:")
            print(r.url)
            print("Response:")
            print(json)
        return json

    def eth_blockNumber(self):
        """The current block number."""
        return self._dispatch(action='eth_blockNumber')

    def eth_getBlockByNumber(self, tag='latest', boolean=False):
        """Gets a block from Etherscan.io

        Arguments:
        tag -- The default block parameter, defaults to 'latest'.
        boolean -- Set to True for more transaction data. Defaults to False.
        """
        return self._dispatch(action='eth_getBlockByNumber',
                              tag=tag,
                              boolean=str(bool(boolean)).lower())

    def eth_getBlockTransactionCountByNumber(self, tag='latest'):
        """Get the number of transactions in a block.

        Argument:
        tag -- The default block parameter, defaults to 'latest'.
        """
        return self._dispatch(action='eth_getBlockTransactionCountByNumber',
                              tag=tag)

    def eth_getTransactionByHash(self, tx_hash):
        """Returns details of a transaction.

        Argument:
        tx_hash -- The hex encoded transaction hash.
        """
        return self._dispatch(action='eth_getTransactionByHash',
                              txhash=tx_hash)

    def eth_getTransactionByBlockNumberAndIndex(self, index, tag='latest'):
        """Get's transaction details on a specific transaction in a block.

        Arguments:
        tag -- The default block parameter, defaults to 'latest'.
        index -- The hex encoded transaction index.
        """
        return self._dispatch(action='eth_getTransactionByBlockNumberAndIndex',
                              tag=tag,
                              index=index)

    def eth_getTransactionCount(self, address, tag='latest'):
        """Get's the number of transactions made by an address.

        Arguments:
        address -- A hex encoded Ethereum address.
        tag -- The default block parameter, defaults to 'latest'.
        """
        return self._dispatch(action='eth_getTransactionCount',
                              address=address,
                              tag=tag)

    def eth_sendRawTransaction(self, tx_hex):
        """Sends a raw transaction.

        Argument:
        tx_hex -- The hex encoded transaction data.
        """
        return self._dispatch(action='eth_sendRawTransaction',
                              hex=tx_hex)

    def eth_getTransactionReceipt(self, tx_hash):
        """Get's the receipt for a transaction.

        Argument:
        tx_hash -- The hex encoded transaction hash.
        """
        return self._dispatch(action='eth_getTransactionReceipt',
                              txhash=tx_hash)

    def eth_call(self, address, data):
        """Returns the result of calling a smart contract.

        Arguments:
        address -- The hex encoded address of the contract.
        data -- Hex encoded ABI data for interacting with the contract.
        """
        return self._dispatch(action='eth_call',
                              to=address,
                              data=data)

    def eth_getCode(self, address, tag='latest'):
        """Get's the byte code of a contract.

        Arguments:
        address -- The hex encoded contract address.
        tag -- The default block parameter, defaults to 'latest'.
        """
        return self._dispatch(action='eth_getCode',
                              address=address,
                              tag=tag)

    def eth_getStorageAt(self, address, position, tag='latest'):
        """Get's a 32 byte value from the address's storage.

        Arguments:
        address -- The hex encoded address who's storage you want to inspect.
        position -- A hex encoded location in the address's storage.
        tag -- The default block parameter, defaults to 'latest'.
        """
        return self._dispatch(action='eth_getStorageAt',
                              address=address,
                              position=position,
                              tag=tag)
