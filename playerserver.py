import sys
from time import sleep

import Pyro.core
import Pyro.naming

from PyQt4.QtCore import *

# exported object that the server uses for callbacks
'''class Player(Pyro.core.ObjBase, QObject):
    
    def __init__(self, name):
        Pyro.core.ObjBase.__init__(self)
        self.name = name

    def greet(self):
        print self.name
'''        
    
# player server thread that assures the gui is responsive
class PlayerServerThread(QThread, Pyro.core.ObjBase):
    
    def __init__(self, username, parent=None):
        Pyro.core.ObjBase.__init__(self)
        super(PlayerServerThread, self).__init__(parent)
        self.username = username

    #def run(self):
    def run(self):
        Pyro.core.initServer()
        ns = Pyro.naming.NameServerLocator().getNS()

        self.daemon = Pyro.core.Daemon()
        self.daemon.useNameServer(ns)

        uri = self.daemon.connect(PlayerServerThread(self.username), self.username)

        print 'The daemon runs on port:', self.daemon.port
        print 'The game\'s URI is:', uri  

        print 'Player Server started'
        #self.daemon.requestLoop()
        #while True:        self.server.exit()
        #    app.processEvents()
        #    daemon.handleRequests()
        #    time.sleep(0.01)
        self.emit(SIGNAL('serverStarted'))
        while True:
            QAbstractEventDispatcher.instance(self).processEvents(QEventLoop.AllEvents)
            self.daemon.handleRequests()
            sleep(0.01)

    def exit(self):
        print 'Player Server exitting'
        #self.daemon.disconnect(self)
        self.daemon.shutdown()

    def greet(self):
        print self.username, 'has been contacted'
        
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
