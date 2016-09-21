import logging

import utils
from strategy.Strategy import Strategy


class UnderdogBaseball(Strategy):

    def __init__(self, *args, **kwargs):
        super(UnderdogBaseball, self).__init__(*args, **kwargs)
        self.name = "UnderdogBaseball"
        self._sport = "Baseball"
        self._leagues = ["MLB"]


    def add_fixture(self, fixture, moneyline):
        away_odd = utils.convert_decimal_to_american(moneyline.get('away'))
        home_odd = utils.convert_decimal_to_american(moneyline.get('home'))
        if max(home_odd, away_odd) < 150:
            logging.info("Adding fixture: %s" % (fixture,))
            self._fixtures.append(fixture)
        else:
            logging.debug("Trash => ", fixture.home, home_odd, fixture.away, away_odd, moneyline)

