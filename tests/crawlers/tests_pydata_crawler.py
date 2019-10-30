from unittest import TestCase, main
from crawlers import PyDataCrawler

import vcr
import logging

logging.basicConfig()
VCR_LOG = logging.getLogger("vcr")
VCR_LOG.setLevel(logging.CRITICAL)


class TestPyData(TestCase):

    @vcr.use_cassette('tests/tapes/tests_collects_data_from_events.yml')
    def tests_collects_data_from_events(self):
        pydata = PyDataCrawler()
        pydata.get_events()

        self.assertEqual(len(pydata.events), 7)

    @vcr.use_cassette('tests/tapes/tests_collects_data_from_events.yml')
    def tests_collects_data_from_events_check_a_existing_event(self):
        pydata = PyDataCrawler()
        events = pydata.get_events()

        self.assertIn('PyData Los Angeles', [event['name'] for event in events])
        self.assertIn('USA', [event['country'] for event in events])
        self.assertIn('California', [event['city'] for event in events])
        self.assertIn('2019-12-03', [event['start_date'] for event in events])
        self.assertIn('https://pydata.org/la2019/', [event['url'] for event in events])


if __name__ == '__main__':
    main()
