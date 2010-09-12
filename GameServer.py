import sys
from time import sleep

import Pyro.core
import Pyro.naming

from PyQt4.QtCore import *

# player server thread that assures the gui is responsive
class GameServer(QThread, Pyro.core.ObjBase):
    
    def __init__(self, parent=None):
        Pyro.core.ObjBase.__init__(self)
        super(PlayerServer, self).__init__(parent)

    def run(self):
        Pyro.core.initServer()
        ns = Pyro.naming.NameServerLocator().getNS()

        self.daemon = Pyro.core.Daemon()
        self.daemon.useNameServer(ns)

        uri = self.daemon.connect(GameServer(), 'jeopardy')

        print 'The daemon runs on port:', self.daemon.port
        print 'The game\'s URI is:', uri  

        print 'Game Server started'

        self.emit(SIGNAL('serverStarted'))
        while True:
            QAbstractEventDispatcher.instance(self).processEvents(QEventLoop.AllEvents)
            self.daemon.handleRequests()
            sleep(0.01)

    def exit(self):
        print 'Game Server exitting'
        self.daemon.shutdown()

    def greet(self):
        print 'Game has been contacted'
        
    def sayHello(self):
        print 'Saying hello from server thread via signal'
        
"""
def main():
    app = QCoreApplication(sys.argv)
    #try:
    server = PlayerServerThread(sys.argv[1])
    #except:
    #    print 'No username supplied!'
    #    sys.exit()

    server.start()
    for i in range(1, 10):
        print 'Testing...', i
    #server.join()
    
    #server.terminate()
    key = 'a'
    while key != 'x':
        key = raw_input('Press \'x\' to terminate Player Server Thread\n')
        if key == 'x':
            server.exit()
        sleep(1)
    #print 'Server thread finished'
    sys.exit()
    app.exec_()

if __name__ == '__main__':
    main()
"""
