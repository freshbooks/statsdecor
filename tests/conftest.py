from mock import patch, Mock
from statsd import StatsClient


def stub_client(path='statsdecor.client'):
    """Factory for StubClient context managers"""
    return StubClient(path)


class StubClient(object):
    """Basic context manager that handles
    stubbing out the statsd client factory in the
    library.
    """
    def __init__(self, path):
        self.patcher = patch(path)

    def __enter__(self):
        self.client = Mock(spec=StatsClient)
        stub_func = self.patcher.start()
        stub_func.return_value = self.client
        return self

    def __exit__(self, ty, value, traceback):
        self.patcher.stop()
