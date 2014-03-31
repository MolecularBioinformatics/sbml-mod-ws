# -*- encoding: UTF-8 -*-
import logging
import logging.handlers

from pyserver.config import SERVERD_LOG_FILE, SERVICE_LOG_FILE, LOG_LEVELS, DEFAULT_LOG_LEVEL, MAX_BYTES, BACKUP_COUNT
        
class ServerLogger():
    def __init__(self, loglevel=DEFAULT_LOG_LEVEL):
        self.log = logging.getLogger('ServerLogger')
        self.log.setLevel(LOG_LEVELS.get(loglevel, logging.NOTSET))
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler = logging.handlers.RotatingFileHandler(SERVERD_LOG_FILE, 
                                                       maxBytes=MAX_BYTES, 
                                                       backupCount=BACKUP_COUNT)
        handler.setFormatter(formatter)
        self.log.addHandler(handler)

class ServiceLogger():
    def __init__(self, loglevel=DEFAULT_LOG_LEVEL):
        self.log = logging.getLogger('ServiceLogger')
        self.log.setLevel(LOG_LEVELS.get(loglevel, logging.NOTSET))
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler = logging.handlers.RotatingFileHandler(SERVICE_LOG_FILE, 
                                                       maxBytes=MAX_BYTES, 
                                                       backupCount=BACKUP_COUNT)
        handler.setFormatter(formatter)
        self.log.addHandler(handler)

        
if __name__ == '__main__':
    logger = ServerLogger()
    logger.log.info('test')