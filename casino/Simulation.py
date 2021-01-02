import json
import logging
import os

from casino.Casino import Casino


class Simulation(Casino):
    def __init__(self, relative_simulation_path, *args, **kwargs):
        super(Simulation, self).__init__(*args, **kwargs)
        self.current_balance = 1000
        self.path = relative_simulation_path

    def get_sports(self):
        raise NotImplementedError

    def get_leagues(self, sport_name):
        raise NotImplementedError

    def _open_json_file(self, file_name):
        json_path = os.path.join(self.path, file_name)
        logging.debug("Open %s" % json_path)
        with open(json_path) as json_file:
            json_data = json.load(json_file)
            json_file.close()
        return json_data

    def get_fixtures(self, sport_name, league_names=[], since=None, is_live=False):
        last = 0
        return last, self._open_json_file('simulation_get_fixtures.json')

    def get_odds(self, sport_name, league_names=[], since=None, is_live=False):
        last = 0
        return last, self._open_json_file('simulation_get_odds.json')

    def get_client_balance(self):
        return self.current_balance

    def get_currencies(self):
        raise NotImplementedError

    def place_bet(self):
        raise NotImplementedError

    def get_bets(self, bet_ids):
        raise NotImplementedError
