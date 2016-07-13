from casino.Pinnacle import Pinnacle

__author__ = 'daniel'

def test_name_of_Pinnacle():
    pinnacle = Pinnacle()

    name = pinnacle.name

    assert name=="Pinnacle"

def test_get_sport_id():
    pinnacle = Pinnacle()
    sport_name = "Soccer"

    sport_id = pinnacle._get_sport_id(sport_name)

    assert sport_id == 29


def test_get_sports():
    pinnacle = Pinnacle()

    sports = pinnacle.get_sports

    assert sports != ""