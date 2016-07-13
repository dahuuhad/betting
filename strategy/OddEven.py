from strategy.Strategy import Strategy

__author__ = 'daniel'

class OddEven(Strategy):

    def __init__(self):
        self.sport = "Soccer"

    def find_games(self):
        for casino in self.casinos:
            balance = casino.get_client_balance()
            casino.get_
