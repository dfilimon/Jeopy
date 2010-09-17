from copy import deepcopy

import Pyro.core
import Pyro.naming

from PyQt4.QtCore import *

mutex = QMutex()

class Game(QThread, Pyro.core.ObjBase):
    playerConnected = pyqtSignal(QString)
    
    def __init__(self, server, parent = None):
        Pyro.core.ObjBase.__init__(self)
        super(Game, self).__init__(parent)
        self.server = server
        self.playerConnected.connect(self.server.gui.adminView.insertItem)
        self.playerConnected.connect(self.server.greet)

    def run(self):
        self.exec_()
        
    def connect(self, name):
        name = str(name)
        if self.server.loginEnabled:
            print 'Game: Connection from:', name
            player = Pyro.core.getProxyForURI('PYRONAME://' + name)
            player._setOneway('greet')
            
            mutex.lock()
            self.server.players[name] = (0,  player)
            mutex.unlock()
            
            print self.server.players[name]
            print 'Game: hello', self, self.server
            self.playerConnected.emit(name)
        
    def greet(self, name):
        print 'Game has been contacted'        

    def getPlayers(self):
        return self.server.players.keys()

    def getResources(self):
        return deepcopy(self.server.resources)
