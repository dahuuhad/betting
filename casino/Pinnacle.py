import base64
import os
import urllib2
import urlparse
import json
import xml.etree.ElementTree as ET
from pprint import pprint
from casino.Casino import Casino


class Pinnacle(Casino):
    def __init__(self, *args, **kwargs):
        super(Pinnacle, self).__init__(*args, **kwargs)
        self._name = "Pinnacle"
        self._user_id = 'DH487342'
        self._password = '2eE22$k&^G'
        self._base_url = "https://api.pinnaclesports.com/v1/"
        self._currency_code = "SEK"
        base_64_str = "Basic " + base64.b64encode(
            '{}:{}'.format(self._user_id, self._password).encode('utf-8')).decode('ascii')
        self._headers = {'Content-length': '0',
                         'Content-type': 'application/xml',
                         'Authorization': base_64_str}

        self._tmp_dir = "pinnacle_tmp"
        if not os.path.isdir(self._tmp_dir):
            os.mkdir(self._tmp_dir)

    def _call(self, url_param, file_name="tmp", use_cache=True):
        """

        :rtype : str
        """
        file_path = os.path.join(self._tmp_dir, file_name)
        url = urlparse.urljoin(self._base_url, url_param)
        if not use_cache or not os.path.isfile(file_path):
            print "Calling %s" % url
            request = urllib2.Request(url, headers=self._headers)
            response_data = urllib2.urlopen(request).read()
            with open(file_path, 'w') as out_file:
                out_file.write(response_data)
        return file_path

    def get_leagues(self, sport_name):
        sport_id = self._get_sport_id(sport_name)
        file_name = 'api_leagues_%s.xml' % sport_id
        url_param = 'leagues?sportid=%s' % sport_id
        file_path = self._call(url_param, file_name, self._use_cache)
        doc = ET.parse(file_path)
        leagues = []
        for league in doc.findall(".//league"):
            leagues.append({'id':league.attrib['id'], 'name':league.text})
        return leagues

    def __build_url(self, url_param, sport_id, league_names, league_ids_str, since, is_live, odds_format=None):
        url = url_param
        if sport_id is not None:
            url += 'sportid=%s&' % sport_id
        if league_names is not None and len(league_names) > 0:
            url += 'leagueids=%s&' % league_ids_str
        if since is not None:
            url += 'since=%s&' % since
        if is_live:
            url += 'islive=1&'
        if odds_format is not None:
            url += 'oddsFormat=%s&' % odds_format
        return url

    def __create_league_ids_str(self, sport_name, league_names):
        league_ids_str = ''
        if league_names is not None and len(league_names) > 0:
            league_ids_str = '_'.join(str(self._get_league_id(sport_name, league)) for league in league_names)
        return league_ids_str

    def __load_json_data(self, file_path):
        with open(file_path) as data_file:
            return json.load(data_file)
        return None

    def get_fixtures(self, sport_name, league_names=[], since=None, is_live=False):
        sport_id = self._get_sport_id(sport_name)
        league_ids_str = self.__create_league_ids_str(sport_name, league_names)
        file_name = 'api_fixtures_%s_%s_%s_%s.json' % (sport_id, league_ids_str, since, is_live)
        url_param = self.__build_url('fixtures?', sport_id, league_names, league_ids_str, since, is_live)
        file_path = self._call(url_param, file_name, False)

        fixtures = self.__load_json_data(file_path)
        last = fixtures.get('last')
        leagues = fixtures.get('league')
        for league in leagues:
            league_id = league.get('id')
            events = league.get('events')
            events[:] = [event for event in events if self.__is_bettable(event) and not self.__parlay_restriction(event)\
                         and (is_live or not self.__is_live_event(event))]

        return last, fixtures

    def __parlay_restriction(self, event):
        return event.get('parlayRestriction') == 1

    def __is_bettable(self, event):
        return event.get('status') != 'H'

    def __is_live_event(self, event):
        return event.get('liveStatus') == 1

    def get_odds(self, sport_name, league_names=[], since=None, is_live=False):
        sport_id = self._get_sport_id(sport_name)
        league_ids_str = self.__create_league_ids_str(sport_name, league_names)
        file_name = 'api_odds_%s_%s_%s_%s.json' % (sport_id, league_ids_str, since, is_live)
        url_param = self.__build_url('odds?', sport_id, league_names, league_ids_str, since, is_live, self._odds_format)
        file_path = self._call(url_param, file_name, self._use_cache)

        odds = self.__load_json_data(file_path)
        return odds


    def get_bets(self, bet_ids):
        pass

    def get_currencies(self):
        pass

    def get_client_balance(self):
        file_name = 'api_client_balance.json'
        url_param = 'client/balance'
        file_path = self._call(url_param, file_name, use_cache=False)
        json_data = open(file_path).read()
        balance  = json.loads(json_data)
        return balance

    def place_bet(self):
        pass


    def _get_sport_id(self, sport_name):
        sports = self.get_sports
        for sport in sports:
            if sport['name'] == sport_name:
                return int(sport['id'])
    def _get_league_id(self, sport_name, league_name):
        leagues = self.get_leagues(sport_name)
        for league in leagues:
            if league.get('name') == league_name:
                return int(league.get('id'))

        return None

    @property
    def get_sports(self):
        file_name = 'api_sports.xml'
        url_param = 'sports'
        file_path = self._call(url_param, file_name, self._use_cache)
        doc = ET.parse(file_path)
        sports = []
        for sport in doc.findall(".//sport"):
            sports.append({'id':sport.attrib['id'], 'name':sport.text})
        return sports

    def _get_league_ids(self, sport_name, league_names):
        # Todo
        pass