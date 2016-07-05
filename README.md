# PyRPCTools
RPC classes for interacting with Ethereum nodes.

PyRPCTools includes three RPC client classes, `HTTPRPC`, `IPCRPC`, and `EtherscanRPC`. The first two are subclasses of the same base class (`JSONRPC`)
and thus behave very similarly. The `EtherscanRPC` is superficially similar to the others but is limited to the supported methods provided by etherscan.io.

The difference between the HTTPRPC and IPCRPC classes is that the former uses HTTP (via the requests module) to conduct the JSON RPC, while the latter uses the faster Unix domain socket interface. 


## JSONRPC derived API

* `rpc_client.send(method, *params, batch=False)`

   Sends a single JSON RPC. If the `batch` keyword is `False`, the JSON RPC is sent immediately to the Ethereum node and the resulting JSON response is returned as a python `dict`. If `batch` is `True` then the JSON RPC is just added to the current batch and nothing is returned. The first argument goes into the `'method'` key of the JSON RPC message, and any extra paramters are simply added to the list in the 'params' key.

* `rpc_client.end_batch()`

   Sends the current batch of JSON RPCs. The result is a list of JSON responses as `dict`s.

Both IPCRPC and HTTPRPC classes allow dynamic generation of convenient functions, for example:
```python
rpc_client.eth_coinbase() # equivalent to rpc_client.send('eth_coinbase')
```
These functions all take a variable amount of arguments, which are all added to their JSON RPC's `'params'` member.
They also take the `batch` keyword argument.

### Etherscan GETH proxy
The class `EtherscanRPC` has an interface similar to the other classes, but it uses the Etherscan GETH proxy API. It is limited to using only the supported rpc methods; see https://etherscan.io/api#proxy for more information.

## Tests

Tests are found in the `tests` directory. To run the tests, first install the requirements in `test-requirements.txt` and run `python -m pytest tests` (this command works with virtualenv) inside whatever folder you cloned/extracted this repo to. You will need to have an Ethereum node running with ipc and http rpc enabled, with the default locations. An internet connection is needed to run the EtherscanRPC tests.
