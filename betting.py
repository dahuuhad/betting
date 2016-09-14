import logging

from casino.Pinnacle import Pinnacle
from data.Spreadsheet import Spreadsheet
from strategy.OddEven import OddEven
from strategy.UnderdogBaseball import UnderdogBaseball

__author__ = 'daniel'


def print_help():
    print "usage: betting"


def setup_logging():
    logging.basicConfig( format='%(asctime)s %(message)s', level=logging.INFO)


def main():
    """

    :rtype : object
    """

    setup_logging()

    spreadsheet = Spreadsheet()

    casinos = [Pinnacle(use_cache = True, odds_format = "DECIMAL")]
    underdog_baseball_strategy =  UnderdogBaseball(spreadsheet, casinos)
    underdog_baseball_strategy.start()

    oddeven_strategy = OddEven(spreadsheet, casinos)
    oddeven_strategy.start()


    return 0


if __name__ == "__main__":
    main()
