class BaseTest(object):
    def make_rpc_client(self):
        raise NotImplementedError("make_rpc_client must be overridden in a subclass.")

    def test_is_valid_json(self):
        rpc_client = self.make_rpc_client()
        good = '{"abc":123}'
        bad = good[:-3]
        assert rpc_client.is_valid_json(good) == True
        assert rpc_client.is_valid_json(bad) == False

    def test_send_rpc(self):
        rpc_client = self.make_rpc_client()
        result = rpc_client.send_rpc('eth_coinbase')
        assert isinstance(result, dict)
        assert all([k in result for k in ('jsonrpc', 'id', 'result')])
        rpc_client.close()

    def test_dynamic_dispatch(self):
        rpc_client = self.make_rpc_client()
        result = rpc_client.eth_coinbase()
        assert isinstance(result, dict)
        assert all([k in result for k in ('jsonrpc', 'id', 'result')])
        rpc_client.close()

    def test_send_batch(self):
        rpc_client = self.make_rpc_client()
        rpc_client.send_rpc('eth_coinbase', batch=True)
        rpc_client.send_rpc('eth_getBlockByNumber', 'earliest', True, batch=True)
        rpc_client.send_rpc('eth_sendTransaction',
                            {'from':0xcafed00d,
                             'to': 0xcafebabe,
                             'value': 1000},
                            batch=True)
        result = rpc_client.send_batch()
        assert isinstance(result, list)
        assert all([isinstance(i, dict) for i in result])
        assert all([k in result[0] for k in ('jsonrpc', 'id', 'result')])
        assert all([k in result[1] for k in ('jsonrpc', 'id', 'result')])
        assert all([k in result[2] for k in ('jsonrpc', 'id', 'error')])
        rpc_client.close()
