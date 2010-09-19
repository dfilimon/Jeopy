from copy import deepcopy

import Pyro.core
import Pyro.naming

from PyQt4.QtCore import *

class Game(QThread, Pyro.core.ObjBase):
    
    playerConnected = pyqtSignal(QString)
    playerDisctonnected = pyqtSignal(QString)
    playerBuzzed = pyqtSignal(QString)
    
    def __init__(self, server, parent = None):
        Pyro.core.ObjBase.__init__(self)
        super(Game, self).__init__(parent)
        self.server = server
        
        self.playerConnected.connect(self.server.gui.adminView.insertItem)
        self.playerConnected.connect(self.server.greet)
        #self.playerBuzzed.connect(self.server.gui.

    def run(self):
        self.exec_()
        
    def connect(self, name):
        name = str(name)
        if self.server.loginEnabled:
            print 'Game: Connection from:', name
            player = Pyro.core.getProxyForURI('PYRONAME://' + name)
            player._setOneway('greet')
            
            self.server.playerMutex.lock()
            self.server.players[name] = (0,  player)
            self.server.playerMutex.unlock()
            
            print self.server.players[name]
            print 'Game: hello', self, self.server
            self.playerConnected.emit(name)

    def disconnect(self, name):
        name = str(name)
        self.server.playerMutex.lock()
        del self.server.players[name]
        self.playerDisconnected.emit(name)
        self.server.playerMutex.unlock()
        
    def greet(self, name):
        print 'Game has been contacted'        

    def getPlayers(self):
        return self.server.players.keys()

    def getResources(self):
        return deepcopy(self.server.resources)

    def getQuestion(self, i, j):
        return self.server.rules['rounds'][self.server.round]['categories'][i]['questions'][j]

    def buzz(self, name):
        self.server.buzzMutex.lock()
        if self.server.buzzed == False:
            self.server.buzzed = True
        else:
            self.server.buzzMutex.unlock()
            return
        self.server.buzzMutex.unlock()
        self.playerBuzzed.emit(name)
        
        
