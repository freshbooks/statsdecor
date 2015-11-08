import statsdecor.decorators as decorators
from tests.conftest import stub_client
from mock import MagicMock


def assert_arguments(args, kwargs):
    assert ('some', 'thing') == args
    assert {'key': 'value'} == kwargs


def test_increment():
    @decorators.increment('a.metric')
    def test_fn(*args, **kwargs):
        assert_arguments(args, kwargs)

    with stub_client('statsdecor.decorators.client') as stub:
        test_fn('some', 'thing', key='value')
        stub.client.incr.assert_called_with('a.metric')


def test_decrement():
    @decorators.decrement('a.metric')
    def test_fn(*args, **kwargs):
        assert_arguments(args, kwargs)

    with stub_client('statsdecor.decorators.client') as stub:
        test_fn('some', 'thing', key='value')
        stub.client.decr.assert_called_with('a.metric')


def test_timed():
    @decorators.timed('a.metric')
    def test_fn(*args, **kwargs):
        assert_arguments(args, kwargs)

    with stub_client('statsdecor.decorators.client') as stub:
        # Stub out the timing context manager.
        stub.client.timer.return_value = MagicMock()
        test_fn('some', 'thing', key='value')
        stub.client.timer.assert_called_with('a.metric')
