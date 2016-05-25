from rpctools import *


def test_rpc(rpc):
    rpc.eth_coinbase()
    rpc.net_version()
    result = rpc.web3_sha3('0x' + 'lol'.encode('hex'))['result']
    assert result == '0xf172873c63909462ac4de545471fd3ad3e9eeadeec4608b92d16ce6b500704cc'


def test_ipc():
    import os

    testnet = os.path.join(os.environ["HOME"],
                           ".testnet",
                           "geth.ipc")
    rpc_client = IPCRPCClient(testnet, True)
    print 'testing IPCRPCClient'
    test_rpc(rpc_client)


def test_http():
    rpc_client = HTTPRPCClient(verbose=True)
    print 'testing HTTPRPCClient'
    test_rpc(rpc_client)


def main():
    test_ipc()
    print
    test_http()


if __name__ == '__main__':
    main()
