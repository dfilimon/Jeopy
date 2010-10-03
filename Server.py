import sys
from time import sleep

import Pyro.core
import Pyro.naming

from PyQt4.QtCore import *

class Server(QThread):
    
    serverStarted = pyqtSignal(str)
    
    def __init__(self, gui, name, parent=None):
        super(Server, self).__init__(parent)
        self.gui = gui
        self.name = name

    def run(self):
        self.connectSignals()
        Pyro.core.initServer()
        ns = Pyro.naming.NameServerLocator().getNS()

        self.daemon = Pyro.core.Daemon()
        self.daemon.useNameServer(ns)
        self.connectDaemon()

        self.log('The daemon runs on port: ' + str(self.daemon.port))
        self.log('The server\'s URI is: ' + str(self.uri))
        self.log('Server started')

        self.serverStarted.emit(self.name)
        while True:
            QAbstractEventDispatcher.instance(self).processEvents(QEventLoop.AllEvents)            
            self.daemon.handleRequests(0)
            sleep(0.01)

    def log(self, message):
        print self.name + ': ' + message
        
    def exit(self):
        self.log('Server exitting')
        self.daemon.shutdown(True)

    def connectSignals(self):
        pass
    def connectDaemon(self):
        pass
