import tabulate

class Casino(object):
    def __init__(self, use_cache=True, odds_format=""):
        self._name = "Casino"
        self._use_cache = use_cache
        self._odds_format = odds_format

    @property
    def name(self):
        return self._name

    def print_casino_info(self):
        #print "*"*10, self.name, "*"*10
        balance = self.get_client_balance()
        return self.name, balance

    def _get_sport_id(self):
        raise NotImplementedError

    def get_sports(self):
        raise NotImplementedError

    def get_leagues(self, sport_name):
        raise NotImplementedError

    def get_fixtures(self, sport_name, league_names=[], since=None, is_live=False):
        raise NotImplementedError

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


class Event(object):
    def __init__(self, json_data):
        self._id = json_data.get('id')
        self._home = json_data.get('home')
        self._away = json_data.get('away')
        self._live_status = json_data.get('liveStatus')
        self._parlay_restriction = json_data.get('parlayRestriction')
        self._starts = json_data.get('starts')
        self._status = json_data.get('status')

    def available_for_betting(self):
        return self._status != "H"

    def __str__(self):
        return "This is an event"

class BaseballEvent(Event):
    def __init__(self, json_data):
        super(BaseballEvent, self).__init__(json_data)
        self._away_pitcher = json_data.get('awayPitcher')
        self._home_pitcher = json_data.get('homePitcher')

    def __str__(self):

        return "This is a baseball event"

