from casino.Casino import Casino

__author__ = 'daniel'
import betfairng

class Betfair(Casino):
    def __init__(self):
        super(Betfair, self).__init__()
        self._name = "Betfair"