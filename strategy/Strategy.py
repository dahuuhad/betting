import json
import logging
import threading
import time
from collections import namedtuple

import feedparser


class Strategy(threading.Thread):

    def __init__(self, datastore, casinos, start_deposit=1000, sleep=60):
        super(Strategy, self).__init__(group=None, target=None, name=None)
        self._datastore = datastore
        self._balance = start_deposit 
        self._fixtures = []
        self._casinos = casinos
        self._leagues = None
        self._is_live = False
        self._sleep = sleep

    def run(self):
        # type: () -> object
        while True:
            try:
                logging.debug("Getting fixtures")
                self.get_fixtures()
            except NoFixturesFound:
                logging.error("No fixtures found")
                logging.debug("Sleeping for some time")
                time.sleep(self._sleep)

    def get_fixtures(self):
        logging.debug("Inside get_fixtures")
        last = 0
        for casino in self._casinos:
            # name, balance = casino.print_casino_info()
            # leagues = casino.get_leagues(sport)
            # print tabulate(leagues)
            last, fixtures = casino.get_fixtures(self._sport, self._leagues, since=last, is_live=self._is_live)
            leagues = fixtures.get('league')
            if not leagues:
                raise NoFixturesFound("")
            possible_fixtures = {}
            for league in leagues:
                league_id = league.get('id')
                logging.debug("League id: %s" % league_id)
                events = league.get('events')
                for event in events:
                    data = json.dumps(event)
                    fixture = json.loads(data, object_hook=lambda d: namedtuple('Fixture', d.keys())(*d.values()))
                    possible_fixtures[fixture.id] = fixture
                    # print tabulate(events, headers='keys', tablefmt='rst')
            last = 0
            odds = casino.get_odds(self._sport, self._leagues, since=last, is_live=self._is_live)
            last = odds.get('last')

            leagues = odds.get('leagues')
            for league in leagues:
                events = league.get('events')
                for event in events:
                    id = event.get('id')
                    fixture = possible_fixtures.get(id)
                    if fixture:
                        moneyline = event.get('periods')[0].get('moneyline')
                        if moneyline:
                            self.add_fixture(fixture, moneyline)

                            # print tabulate(event, headers='keys', tablefmt='rst')

    def add_fixture(self, fixture, moneyline):
        raise NotImplementedError

class NoFixturesFound(Exception):
    pass

class Sharps():
    def __init__(self, feed_id):
        self._username = "dahuuhad"
        self._password = "secret"
        self._feed = "http://www.sharps.se/spreadsheet/rss/%s.rss" % feed_id
        d = feedparser.parse(self._feed)
        for entry in d.entries:
            logging.info(entry.summary_detail.value)

