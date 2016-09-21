from casino.Casino import Casino

class Simulation(Casino):
    def __init__(self, *args, **kwargs):
        super(Simulation, self).__init__(*args, **kwargs)


    def get_sports(self):
        raise NotImplementedError

    def get_leagues(self, sport_name):
        raise NotImplementedError

    def get_fixtures(self, sport_name, league_names=[], since=None, is_live=False):
        last = 0
        fixtures = {}
        return last, fixtures

    def get_odds(self, sport_name, league_names=[], since=None, is_live=False):
        raise NotImplementedError

    def get_client_balance(self):
        raise NotImplementedError

    def get_currencies(self):
        raise NotImplementedError

    def place_bet(self):
        raise NotImplementedError

    def get_bets(self, bet_ids):
        raise NotImplementedError
