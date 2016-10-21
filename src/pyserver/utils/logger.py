# -*- encoding: UTF-8 -*-

# SBMLmod Web Service
# Copyright (C) 2016 Computational Biology Unit, University of Bergen and
#               Molecular Bioinformatics, UiT The Arctic University of Norway
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

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
