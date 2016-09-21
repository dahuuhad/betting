import logging
import time

from casino.Pinnacle import Pinnacle
from casino.Simulation import Simulation
from data.DataStore import DataStore
from strategy.OddEven import OddEven
from strategy.UnderdogBaseball import UnderdogBaseball

__author__ = 'daniel'


def print_help():
    print "usage: betting"


def setup_logging():
    logging.basicConfig( format='%(asctime)s %(levelname)s (%(threadName)-20s) %(module)s::%(funcName)s (%(lineno)d) - %(message)s', level=logging.DEBUG)


def hello():
    logging.info("Hello")

def world():
    logging.info("World")

def main():
    """

    :rtype : object
    """

    setup_logging()

    logging.debug("Setup the datastore")
    datastore = DataStore()

    logging.debug("Adding casinos")
    casinos = []
    pinnacle = Pinnacle(use_cache = True, odds_format = "DECIMAL")
    simulation = Simulation()
    casinos.append(simulation)

    try:
        strategies = []
        sleep = 10
        strategies.append(UnderdogBaseball(datastore, casinos, sleep=sleep))
        strategies.append(OddEven(datastore, casinos, sleep=sleep))

        logging.debug("Running the strategies")
        for strategy in strategies:
            strategy.start()
            time.sleep(2)
    except KeyboardInterrupt:
        logging.info("User aborted, exiting...")
    return 0


if __name__ == "__main__":
    main()
