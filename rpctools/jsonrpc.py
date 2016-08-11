"""Base class for JSONRPC 2.0 clients."""
from __future__ import print_function
import json


def is_valid_json(stuff):
    """Checks if a string is valid json."""
    try:
        json.loads(stuff)
    except:
        return False
    else:
        return True


class RPCError(Exception):
    pass


class JSONRPC(object):
    """A JSON RPC base class."""

    def __init__(self, verbose):
        self.verbose = verbose
        self.message_number = -1
        self.batch = []

    def _send(self, message):
        # Sends json rpc to the server.
        raise NotImplementedError('_send must be implemented in a subclass.')

    def _send_json_message(self, message):
        # Sends a json message and returns the result.
        encoded_json = json.dumps(message)
        if self.verbose:
            print('Sending JSON:')
            print(encoded_json)

        response = self._send(encoded_json.encode("utf8")).decode("utf8")
        if self.verbose:
            print('Got JSON:')
            print(response)

        return json.loads(response)

    def send(self, method, *params, **kwds):
        """Creates a json message with the given method and params.

        The only keyword accepted is 'batch', which should be True if
        the RPC should be added to the batch. If added to a batch then
        None is returned and the messaged isn't sent until end_batch is called.
        """
        batch = kwds.get('batch', False)
        self.message_number += 1
        rpc = {'jsonrpc': '2.0',
               'id': self.message_number,
               'method': method,
               'params': params}

        if batch:
            self.batch.append(rpc)
        else:
            return self._send_json_message(rpc)

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

            Keyword Argument:
            batch -- Tells whether or not to add to the current batch.
            The default is False.
            """
            batch = kwds.get('batch', False)
            return self.send(method, *params, **{'batch': batch})
        func.__name__ = method
        func.__doc__ = func.__doc__.format(method)
        setattr(self, method, func)
        return func
