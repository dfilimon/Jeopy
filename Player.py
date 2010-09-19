import os, tempfile
import Pyro.core
import Pyro.naming

from PyQt4.QtCore import *

mutex = QMutex()

class Player(QThread, Pyro.core.ObjBase):
    connected = pyqtSignal()
    
    def __init__(self, server, parent = None):
        Pyro.core.ObjBase.__init__(self)
        super(Player, self).__init__(parent)
        self.server = server
        #self.playerConnected.connect(self.gui.adminView.insertItem)
        #self.playerConnected.connect(self.server.greet)

    def greet(self):
        print self.server.name, 'has been contacted'

    def hello(self):
        print 'hello'

    def loadResources(self):
        mutex.lock()
        self.server.resources = self.server.game.getResources()
        self.server.tempPath = tempfile.mkdtemp()
        for resource in self.server.resources.items():
            print 'Player: transferring:', resource[0]
            f = open(self.server.tempPath + '/' + resource[0], 'w')
            f.write(resource[1])
            f.close()
        mutex.unlock()

    def getScore(self):
        return self.server.score

    def getName(self):
        return self.server.name

