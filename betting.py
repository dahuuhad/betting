from pprint import pprint
from casino.Betfair import Betfair
from casino.Pinnacle import Pinnacle
from casino.Casino import BaseballEvent
from data.Spreadsheet import Spreadsheet
from strategy.TwoSixBaseball import TwoSixBaseball
from tabulate import tabulate

__author__ = 'daniel'


def print_help():
    print "usage: betting"


def main():
    """

    :rtype : object
    """

    strategy =  TwoSixBaseball()
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
        #pprint(fixtures)
        leagues = fixtures.get('league')
        for league in leagues:
            league_id = league.get('id')
            print "League id: %s" % league_id
            events = league.get('events')
            print tabulate(events, headers='keys', tablefmt='rst    ')
        odds = casino.get_odds(sport, [league_mlb], is_live=is_live)
        pprint(odds)

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
