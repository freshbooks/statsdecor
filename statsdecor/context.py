from statsdecor import client
import logging
from time import time


_log = logging.getLogger(__name__)


class StatsContext(object):
    """
        Usage example:

        class ThingyStatsContext(StatsContext):
            def __init__(self, tags=None):
                tags = tags or []
                tags += ['service:thingy']
                super(ThingyStatsContext, self).__self__('thingy_client', tags=tags)

            def exit_hook(self, exc_type, exc_val, exc_tb):
                if isinstance(exc_val, PermissionDenied):
                    self.add_tags('result', 'permissiondenied')
                elif exc_val is not None:
                    self.add_tags('result', 'exception')
                else:
                    self.add_tags('result', 'success')

        def call_thing():
            with ThingyStatsContext() as stats:
                result = CallThingy()
                stats.add_tags('status_code', 'result["status_code"]')
    """

    def __init__(self, metric_base, tags=None, stats=None):
        """
            metric_base is add to the beginning of the "attempted", "duration", and "completed" metrics emited.

            tags is a list of string tags (in the format ["key:value", ..])
        """
        self._metric_base = metric_base

        self._tags = tags or []

        self._metric_attempted = '{}.attempted'.format(self._metric_base)
        self._metric_duration = '{}.duration'.format(self._metric_base)
        self._metric_completed = '{}.completed'.format(self._metric_base)

        self._stats = stats or client()

        self._elapsed = None

    def add_tag(self, key, value):
        """ Adds a datadog tag to the metrics emitted.

        Syntatic sugar equivalent to:

            add_tags('{}.{}'.format(key, value))
        """

        self.add_tags('{}:{}'.format(key, value))

    def add_tags(self, *tags):
        """ Adds a datadog tag to the metrics emitted.

        Tags added before the context begins are included in all metrics.
        Tags added before the context finished are included in the 'completed' and 'duration' metrics.
        """
        self._tags.extend(tags)

    def exit_hook(self, exc_type, exc_val, exc_tb):
        """ Called on exit.  By default does nothing.

        Child classes should override this method and translate the exceptions thrown
        (or lack of exceptions thrown) into metric tags.
        """

        pass

    def _start_timer(self):
        self._start = time()

    def _stop_timer(self):
        self._elapsed = time() - self._start

    def __enter__(self):
        self._stats.increment(self._metric_attempted, tags=self._tags)
        self._start_timer()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_timer()
        try:
            self.exit_hook(exc_type, exc_val, exc_tb)
        except Exception:
            # swallow errors--we don't want to complicate exception handling in the main
            # program flow.
            _log.exception("warning: Unhandled expcetion in StatsContext exit hook (ignoring)")

        self._stats.timing(self._metric_duration, self._elapsed, tags=self._tags)
        self._stats.increment(self._metric_completed, tags=self._tags)
        _log.info('Metrics sent: {}, tags={}, elapsed time={}'.format(
            self._metric_base,
            ','.join(self._tags),
            self._elapsed
        ))
        return False
