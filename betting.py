from pprint import pprint
from casino.Betfair import Betfair
from casino.Pinnacle import Pinnacle
from casino.Casino import BaseballEvent
from data.Spreadsheet import Spreadsheet
from strategy.UnderdogBaseball import UnderdogBaseball
from tabulate import tabulate

import json
from collections import namedtuple
import logging

__author__ = 'daniel'


def print_help():
    print "usage: betting"





def main():
    """

    :rtype : object
    """

    logging.basicConfig( format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Started')

    strategy =  UnderdogBaseball()
    #strategy.start()
    use_cache = True
    is_live = False
    sport = "Baseball"
    league_mlb = "MLB"
    odds_format = "DECIMAL"
    last = None
    casinos = [Pinnacle(use_cache, odds_format)]
    for casino in casinos:
        #name, balance = casino.print_casino_info()
        #leagues = casino.get_leagues(sport)
        #print tabulate(leagues)
        last, fixtures = casino.get_fixtures(sport, [league_mlb], since=last, is_live=is_live)
        leagues = fixtures.get('league')
        possible_fixtures = {}
        for league in leagues:
            league_id = league.get('id')
            logging.debug("League id: %s" % league_id)
            events = league.get('events')
            for event in events:
                data = json.dumps(event)
                fixture = json.loads(data, object_hook=lambda d: namedtuple('Fixture', d.keys())(*d.values()))
                possible_fixtures[fixture.id] = fixture
            #print tabulate(events, headers='keys', tablefmt='rst')
        last = 0
        odds = casino.get_odds(sport, [league_mlb], since=last, is_live=is_live)
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
                        strategy.add_fixture(fixture, moneyline)

                #print tabulate(event, headers='keys', tablefmt='rst')
    # pinnacle = Pinnacle()
    # pinnacle.print_casino_info()
    # pinnacle.get_sports()
    #
    # betfair = Betfair()
    # betfair.print_casino_info()


    #spreadsheet = Spreadsheet()

    return 0


if __name__ == "__main__":
    main()
