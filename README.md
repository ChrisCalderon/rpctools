# PyRPCTools
RPC classes for interacting with Ethereum nodes.

PyRPCTools includes two RPC client classes, `HTTPRPCClient` and `IPCRPCClient`.
Both classes expose the exact same API, the only difference being that `HTTPRPCClient` communicates with an Ethereum node through HTTP, while `IPCRPCClient` uses geth's Unix domain socket. `IPCRPCClient` currently only works on *nix with geth.

## API

* `rpc_client.send_rpc(method, *params, batch=False)`
... Sends a single JSON RPC. If `batch` is `False`, the JSON RPC is sent immediately to the Ethereum node and the resulting JSON response is returned as a python `dict`. If `batch` is `True` then the JSON RPC is just added to the current batch.

* `rpc_client.send_batch()`
... Sends the current batch of JSON RPCs. The result is a list of JSON responses as `dict`s.

Both classes also allow dynamic generation of convenient functions, for example:
```python
rpc_client.eth_coinbase() # equivalent to rpc_client.send_rpc('eth_coinbase')
```
These functions all take a variable amount of arguments, which are all added to their JSON RPC's "param" member.
They also take the `batch` keyword argument.
