"""
Runs performance tests to determine if a significant performance regression has
been introduced to the MongoBackend.
"""

from __future__ import absolute_import

from uuid import uuid4

from eventtracking.backends.tests import PerformanceTestCase
from eventtracking.backends.mongodb import MongoBackend
from eventtracking.tracker import Tracker
from six.moves import range


class TestBackendPerformance(PerformanceTestCase):
    """
    Makes use of real backend systems to see how long it takes for the backend
    to commit events to stable storage.
    """

    def setUp(self):
        super(TestBackendPerformance, self).setUp()
        self.database_name = 'perf_test_eventtracking_' + str(uuid4())
        self.mongo_backend = MongoBackend(database=self.database_name)
        self.tracker = Tracker({
            'mongo': self.mongo_backend
        })

    def tearDown(self):
        self.mongo_backend.connection.drop_database(self.database_name)
        super(TestBackendPerformance, self).tearDown()

    def test_sequential_events(self):
        with self.assert_execution_time_less_than_threshold():
            for i in range(self.num_events):
                self.tracker.emit('perf.event', {
                    'sequence': i,
                    'payload': self.random_payload
                })
