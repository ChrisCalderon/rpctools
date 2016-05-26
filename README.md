# PyRPCTools
RPC classes for interacting with Ethereum nodes.

PyRPCTools includes two RPC client classes, `HTTPRPCClient` and `IPCRPCClient`.
Both classes expose the exact same API, the only difference being that `HTTPRPCClient` communicates with an Ethereum node through HTTP, while `IPCRPCClient` uses geth's Unix domain socket. `IPCRPCClient` currently only works on *nix with geth.

## API

* `rpc_client.send_rpc(method, *params, batch=False)`

   Sends a single JSON RPC. If `batch` is `False`, the JSON RPC is sent immediately to the Ethereum node and the resulting JSON response is returned as a python `dict`. If `batch` is `True` then the JSON RPC is just added to the current batch.

* `rpc_client.send_batch()`

   Sends the current batch of JSON RPCs. The result is a list of JSON responses as `dict`s.

Both classes also allow dynamic generation of convenient functions, for example:
```python
rpc_client.eth_coinbase() # equivalent to rpc_client.send_rpc('eth_coinbase')
```
These functions all take a variable amount of arguments, which are all added to their JSON RPC's "param" member.
They also take the `batch` keyword argument.

## Instantiation

In order to use `IPCRPCClient`, you must know the path to your geth node's ipc socket. But don't worry, `IPCRPCClient` already knows about the default geth ipc socket, `~/.ethereum/geth.ipc`. If you call IPCRPCClient without any arguments, it will try to connect to the default. 

`HTTPRPCClient` will do the same; if called without an argument, it will try to connect to `('localhost', 8545)` for RPC. You can specify a different address using `('host', port)`.

Both classes also have a `verbose` argument, which is `False` by default. If you set it to `True`, then every JSON RPC and response will be printed out to the terminal.

## Tests

Tests are found in the `tests` directory. To run the tests, you should install pytest, either to your system or a virtualenv, and then run `py.test tests` in a terminal, inside whatever folder you cloned/extracted this repo to.
