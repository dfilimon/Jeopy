import os
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
        #print 'hello'
        #print self.server.resources.keys()
        try:
            os.mkdir('tmp')
        except:
            pass
        for resource in self.server.resources.items():
            print 'Player: transferring:', resource[0]
            f = open('tmp/' + resource[0], 'w')
            f.write(resource[1])
            f.close()
        mutex.unlock()

