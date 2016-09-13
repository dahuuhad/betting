import betting

__author__ = 'daniel'


def test_convert_200_to_decimal():
    assert 3.00 == betting.convert_american_to_decimal(200)


def test_convert_600_to_decimal():
    assert 7.00 == betting.convert_american_to_decimal(600)

#def test_convert_minus_130_to_decimal():
#    assert 1.769 == betting.convert_american_to_decimal(-130)


def test_convert_2_50_to_american():
    assert 150 == betting.convert_decimal_to_american(2.50)


def test_convert_5_40_to_american():
    assert 440 == betting.convert_decimal_to_american(5.40)
