from rpctools import EtherscanRPC
from rpctools.etherscan import HEX, EtherscanRPCError
import pytest

# TODO: Add checks for EtherscanRPCError being raised at the right time


class Test:
    apikey = 'SDBX686DEWS89RUTT6331U41Y74FA93AQR'  # apikey prevents rate limiting
    bad = {'status': '0', 'message': 'NOTOK', 'result': 'Error!'}  # standard error response from etherscan
    txhash = '0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1'  # txhash used on etherscan page.
    contract = '0xaeef46db4855e25702f8237e8f403fddcaf931c0'  # a contract address for the Etherscan api page.

    @staticmethod
    def response_check(response):
        assert isinstance(response, dict)
        assert response != Test.bad
        assert 'jsonrpc' in response
        assert 'id' in response
        assert 'result' in response

    @classmethod
    def make_rpc(cls):
        return EtherscanRPC(cls.apikey, False)

    def test_eth_blockNumber(self):
        rpc = Test.make_rpc()
        resp = rpc.eth_blockNumber()
        Test.response_check(resp)
        assert HEX.match(resp['result'])

    def test_eth_getBlockByNumber(self):
        rpc = Test.make_rpc()
        resp = rpc.eth_getBlockByNumber(0x10d4f, False)
        Test.response_check(resp)

    def test_eth_getBlockTransactionCountByNumber(self):
        rpc = Test.make_rpc()
        resp = rpc.eth_getBlockTransactionCountByNumber(1800000)
        Test.response_check(resp)

    def test_eth_getTransactionByHash(self):
        rpc = Test.make_rpc()
        resp = rpc.eth_getTransactionByHash(Test.txhash)
        Test.response_check(resp)

    def test_eth_getTransactionByBlockNumberAndIndex(self):
        rpc = Test.make_rpc()
        resp = rpc.eth_getTransactionByBlockNumberAndIndex(460857, 2)
        Test.response_check(resp)

    def test_eth_getTransactionCount(self):
        rpc = Test.make_rpc()
        resp = rpc.eth_getTransactionCount("0x2910543af39aba0cd09dbb2d50200b3e800a63d2", 0x1bdbb4)
        Test.response_check(resp)

    def test_eth_sendRawTransaction(self):
        rpc = Test.make_rpc()
        # TODO: finish this in a way that doesn't spend all my money :p

    def test_eth_getTransactionReceipt(self):
        rpc = Test.make_rpc()
        resp = rpc.eth_getTransactionReceipt(Test.txhash)
        Test.response_check(resp)

    def test_eth_call(self):
        rpc = Test.make_rpc()
        data = '0x70a08231000000000000000000000000e16359506c028e51f16be38986ec5746251e9724'
        resp = rpc.eth_call(Test.contract, data)
        Test.response_check(resp)

    def test_eth_getCode(self):
        rpc = Test.make_rpc()
        resp = rpc.eth_getCode(Test.contract, 'latest')
        Test.response_check(resp)

    def test_eth_getStorageAt(self):
        rpc = Test.make_rpc()
        resp = rpc.eth_getStorageAt(Test.contract, 0, 'latest')
        Test.response_check(resp)
