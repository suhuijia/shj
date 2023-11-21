import logging
import sys
import copy


class LogSelf(object):
    logger = None

    @staticmethod
    def logInit():
        format = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(format)
        logg = logging.getLogger()
        logg.addHandler(handler)
        logg.setLevel(logging.INFO)
        LogSelf.logger = logg

    @staticmethod
    def getLogger():
        # return copy.deepcopy(LogSelf.logger)
        return LogSelf.logger
