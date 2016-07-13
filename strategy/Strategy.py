class Strategy(object):

    def __init__(self, start_deposit=1000, casinos=[]):
        self.balance = start_deposit
        self.casinos = casinos

