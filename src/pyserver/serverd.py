# -*- encoding: UTF-8 -*-
from SocketServer import ThreadingMixIn
from ZSI import ServiceContainer
import sys
import warnings

from pyserver.config import DEFAULT_LOG_LEVEL, SERVERD_PID_FILE, WS_PORT, SERVERD_LOG_FILE
from pyserver.utils.daemon import Daemon
from pyserver.utils.logger import ServerLogger
from sbmlmod.SBMLmod import SBMLmodWS


warnings.filterwarnings('ignore', category=DeprecationWarning)




SERVICES = [SBMLmodWS(),
            ]

class ThreadingServiceContainer(ThreadingMixIn, ServiceContainer.ServiceContainer):
    pass

class MyDaemon(Daemon):
    def AsServer(self, port=80, services=()):
        '''port --
           services -- list of service instances
        '''
        address = ('', port)
        tsc = ThreadingServiceContainer(address, services)
        # for service in services:
        #    path = service.getPost()
        #    sc.setNode(service, path)
        tsc.serve_forever()

    def run(self, loglevel=DEFAULT_LOG_LEVEL):
        self._logger = ServerLogger(loglevel)
        self._logger.log.info('--- STARTING WEB SERVICE DAEMON ---')
        self.AsServer(port=WS_PORT, services=SERVICES)

def serverd():
    daemon = MyDaemon(SERVERD_PID_FILE)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'debug' == sys.argv[1]:
            daemon.run('debug')
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart|debug" % sys.argv[0]
        sys.exit(2)

if __name__ == "__main__":
    serverd()
