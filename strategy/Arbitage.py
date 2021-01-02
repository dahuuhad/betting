import logging

from strategy.Strategy import Strategy


class Arbitage(Strategy):


    def __init__(self, *args, **kwargs):
        super(Arbitage, self).__init__(*args, **kwargs)
        self.name = "Arbitage"
        self._sport = "Tennis"


    def add_fixture(self, fixture, moneyline):
        logging.debug("Adding fixture %s" % fixture)
        self._fixtures.append(fixture)