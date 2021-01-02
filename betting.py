import logging
import time

from casino.Pinnacle import Pinnacle
from data.DataStore import DataStore
from strategy.Arbitage import Arbitage

__author__ = 'daniel'


def print_help():
    print("usage: betting")


def setup_logging(level=logging.DEBUG):
    logging.basicConfig( format='%(asctime)s %(levelname)s (%(threadName)-20s) %(module)s::%(funcName)s (%(lineno)d) - %(message)s', level=level)


def main():
    """

    :rtype : object
    """

    setup_logging(logging.DEBUG)

    logging.info("Setup the datastore")
    datastore = DataStore()

    logging.info("Adding casinos")
    casinos = []
    pinnacle = Pinnacle(use_cache = False, odds_format = "DECIMAL")
    casinos.append(pinnacle)
    relative_simulation_path = "casino"
    #simulation = Simulation(relative_simulation_path)
    #casinos.append(simulation)

    try:
        strategies = []
        sleep = 60
        #strategies.append(UnderdogBaseball(datastore, casinos, sleep=sleep))
        #strategies.append(OddEven(datastore, casinos, sleep=sleep))
        strategies.append(Arbitage(datastore, casinos, sleep=sleep))

        logging.info("Running the strategies")
        for strategy in strategies:
            logging.debug("Starting strategy %s" % strategy)
            strategy.start()
            time.sleep(2)
    except KeyboardInterrupt:
        logging.error("User aborted, exiting...")
    return 0


if __name__ == "__main__":
    main()
