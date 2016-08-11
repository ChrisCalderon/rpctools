class BaseTest(object):

    def make_rpc_client(self):
        err_msg = "make_rpc_client must be overridden in a subclass."
        raise NotImplementedError(err_msg)

    def test_send_rpc(self):
        rpc_client = self.make_rpc_client()
        result = rpc_client.send('eth_coinbase')
        assert isinstance(result, dict)
        assert all([k in result for k in ('jsonrpc', 'id', 'result')])

    def test_dynamic_dispatch(self):
        rpc_client = self.make_rpc_client()
        result = rpc_client.eth_coinbase()
        assert isinstance(result, dict)
        assert all([k in result for k in ('jsonrpc', 'id', 'result')])

    def test_send_batch(self):
        rpc_client = self.make_rpc_client()
        rpc_client.send('eth_coinbase', batch=True)
        rpc_client.send('eth_getBlockByNumber', 'earliest', True, batch=True)
        rpc_client.send('eth_sendTransaction',
                        {'from': 0xcafed00d,
                         'to': 0xcafebabe,
                         'value': 1000},
                        batch=True)
        result = rpc_client.end_batch()
        assert isinstance(result, list)
        assert all([isinstance(i, dict) for i in result])
        assert all([k in result[0] for k in ('jsonrpc', 'id', 'result')])
        assert all([k in result[1] for k in ('jsonrpc', 'id', 'result')])
        assert all([k in result[2] for k in ('jsonrpc', 'id', 'error')])
