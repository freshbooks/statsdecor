import statsdecor
from tests.conftest import stub_client


def test_incr():
    with stub_client() as stub:
        statsdecor.incr('a.metric')
        stub.client.incr.assert_called_with('a.metric', 1, 1)


def test_incr__with_value_and_rate():
    with stub_client() as stub:
        statsdecor.incr('a.metric', 9, 0.1)
        stub.client.incr.assert_called_with('a.metric', 9, 0.1)


def test_decr():
    with stub_client() as stub:
        statsdecor.decr('a.metric')
        stub.client.decr.assert_called_with('a.metric', 1, 1)


def test_decr__with_value_and_rate():
    with stub_client() as stub:
        statsdecor.decr('a.metric', 9, 0.1)
        stub.client.decr.assert_called_with('a.metric', 9, 0.1)


def test_gauge():
    with stub_client() as stub:
        statsdecor.gauge('a.metric', 8)
        stub.client.gauge.assert_called_with('a.metric', 8, 1)


def test_gauge__with_value_and_rate():
    with stub_client() as stub:
        statsdecor.gauge('a.metric', 9, 0.1)
        stub.client.gauge.assert_called_with('a.metric', 9, 0.1)


def test_timer():
    with stub_client() as stub:
        statsdecor.timer('a.metric')
        assert stub.client.timer.called, 'Should be called'
