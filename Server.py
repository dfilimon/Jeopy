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

        self.status('The daemon runs on port: ' + str(self.daemon.port))
        self.status('The server\'s URI is: ' + str(self.uri))
        self.status('Server started')

        self.serverStarted.emit(self.name)
        while True:
            QAbstractEventDispatcher.instance(self).processEvents(QEventLoop.AllEvents)            
            self.daemon.handleRequests(0)
            sleep(0.01)

    def status(self, message):
        print self.name + ': ' + message
        
    def exit(self):
        status('Server exitting')
        self.daemon.shutdown()

    def connectSignals(self):
        pass
    def connectDameon(self):
        pass
