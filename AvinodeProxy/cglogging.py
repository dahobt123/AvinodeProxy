# Common looging environmnet setup
import logging
import os
import sys


class cglogging:

    def __init__(self, level='' ):
        self.level = level
        return

    def setup_logging(self):

        try:

            CAG_Logging = os.environ['CAG_Logging']
            print('We are in Lambda with CAG logging level= {}'.format(CAG_Logging))
        except:
            CAG_Logging = 'debug'
            print('We are in Screen Execution CAG logging level= {}'.format(CAG_Logging))

        logger = logging.getLogger()

        for h in logger.handlers:
            logger.removeHandler(h)

        h = logging.StreamHandler(sys.stdout)

        # use whatever format you want here
        FORMAT = '%(name)s-%(asctime)s %(message)s'
        h.setFormatter(logging.Formatter(FORMAT))
        logger.addHandler(h)

        if CAG_Logging == 'debug' :
            logger.setLevel(logging.DEBUG)
        elif CAG_Logging == 'info' :
            logger.setLevel(logging.INFO)
        elif CAG_Logging == 'critical' :
            logger.setLevel(logging.CRITICAL)
        elif CAG_Logging == 'error' :
            logger.setLevel(logging.ERROR)
        elif CAG_Logging == 'warning' :
            logger.setLevel(logging.WARNING)
        else:
            logger.setLevel(logging.DEBUG)

        return logger
