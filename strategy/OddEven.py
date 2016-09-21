from strategy.Strategy import Strategy, Sharps


__author__ = 'daniel'

class OddEven(Strategy):

    def __init__(self, *args, **kwargs):
        super(OddEven, self).__init__(*args, **kwargs)
        self.name = "OddEven"
        self._sport = "Soccer"

    def add_fixture(self, fixture, moneyline):
        sharps = Sharps(15593)
        self._fixtures.append(fixture)



