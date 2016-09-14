from strategy.Strategy import Strategy

__author__ = 'daniel'

class OddEven(Strategy):

    def __init__(self, *args, **kwargs):
        super(OddEven, self).__init__(*args, **kwargs)
        self._sport = "Soccer"

    def add_fixture(self, fixture, moneyline):
        self._fixtures.append(fixture)