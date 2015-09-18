import logging
import os
LOGPATH=os.path.dirname(os.path.dirname(os.path.dirname(os.path.split(os.path.realpath(__file__))[0])))


class Logger(object):

    logging.basicConfig(filename=LOGPATH + '/logs/omega.log', level='INFO', format='[%(asctime)s] %(levelname)s "%(message)s"',
                        datefmt='%d/%b/%Y %H:%M:%S')
    _logger = logging.getLogger('omegaLogger')

    @classmethod
    def info(cls, msg):
        cls._logger.info(msg)

    @classmethod
    def warning(cls, msg):
        cls._logger.warning(msg)

    @classmethod
    def error(cls, msg):
        cls._logger.error(msg)
