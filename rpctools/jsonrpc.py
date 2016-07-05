"""Base class for JSONRPC 2.0 clients."""
import ujson


def is_valid_json(stuff):
    """Checks if a string is valid json."""
    try:
        ujson.decode(stuff)
    except:
        return False
    else:
        return True


class RPCError(Exception): pass


class JSONRPC(object):
    """A JSON RPC base class.

    Attributes:
    verbose -- A bool which controls whether or not JSON messages are logged.
    message_number -- The number of JSON messages sent, used as a suffix for the id.
    batch -- A list of JSON messages in the current batch.

    Methods:
    rpc.send(method, *params, **kwds) -- Creates and sends a JSON RPC message and returns the response.
    rpc.end_batch() -- Sends the current batch of JSON RPC messages.

    Classes  derived from this class can also generate specialized functions for sending a particular
    JSON RPC method, on the fly. For example rpc.eth_blockNumber() will generate a function called
    eth_blockNumber which sends an RPC with the method eth_blockNumber. These functions allow for
    an arbitrary amount of arguments; the proper arguments to use depend on the RPC used.
    See https://github.com/ethereum/wiki/wiki/JSON-RPC for more info on those. The on-the-fly functions
    also have support for the 'batch' keyword, which adds the call to the current batch instead of
    immediately sending it.
    """
    
    def __init__(self, verbose):

        self.verbose = verbose
        self.message_number = -1
        self.batch = []

    def _send(self, message):
        # Sends json rpc to the server.
        raise NotImplementedError('_send must be implemented in a subclass.')

    def _send_json_message(self, json):
        # Sends a json message and returns the result.
        encoded_json = ujson.encode(json)
        if self.verbose:
            print 'Sending JSON:'
            print encoded_json

        response = self._send(encoded_json.encode("utf8")).decode("utf8")
        if self.verbose:
            print 'Got JSON:'
            print response

        return ujson.decode(response)

    def send(self, method, params, **kwds):
        """Creates a json message with the given method and params,
        then sends it or adds it to the current batch.

        The only keyword accepted is 'batch', which should be True if
        the RPC should be added to the batch"""
        batch = kwds.get('batch', False)
        self.message_number += 1
        json = {'jsonrpc': '2.0',
                'id': self.message_number,
                'method': method,
                'params': params}

        if batch:
            self.batch.append(json)
        else:
            return self._send_json_message(json)

    def end_batch(self):
        """Sends the current JSON RPC batch and starts a fresh one."""
        if self.batch:
            result = self._send_json_message(self.batch)
            self.batch = []
            return result

    def __getattr__(self, method):
        # generates specialized functions on-the-fly.
        def func(*params, **kwds):
            """Convenience function for the '{}' rpc.
            Setting the `batch` keyword argument to True adds to the current batch.
            """
            batch = kwds.get('batch', False)
            return self.send(method, *params, **{'batch':batch})
        func.__name__ = method
        func.__doc__ = func.__doc__.format(method)
        setattr(self, method, func)
        return func
