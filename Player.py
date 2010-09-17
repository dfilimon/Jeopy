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

