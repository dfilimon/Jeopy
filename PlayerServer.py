import sys
from time import sleep
from socket import gethostbyname, gethostname

import Pyro.core
import Pyro.naming

from PyQt4.QtCore import *

from Server import Server
from Player import Player

class PlayerServer(Server):

    playerConnected = pyqtSignal()
    playerStatusChanged = pyqtSignal(str)
    
    gameStarted = pyqtSignal()
    buzzDisabled = pyqtSignal()

    def __init__(self, gui, name, parent=None):
        Server.__init__(self, gui, name)
        self.game = Pyro.core.getProxyForURI('PYRONAME://' + 'jeopardy')
        self.running = False

        self.name = name
        self.ip = gethostbyname(gethostname())

    def run(self):
        self.running = True
        Server.run(self)

    def setupSignals(self):
        self.serverStarted.connect(self.connect)
        self.gameStarted.connect(self.gui.startGame)

    def setupGuiSignals(self):
        Server.setupGuiSignals(self)
        self.playerStatusChanged.connect(self.gui.updateStatus)
        self.buzzDisabled.connect(self.gui.disableBuzz)

    def connectDaemon(self):
        self.uri = self.daemon.connectPersistent(Player(self), self.name)

    def startGame(self):
        self.setupGuiSignals()

    def connect(self):
        self.log('Connecting to server')
        self.game.connect(self.name)
        self.playerConnected.emit()
    
    def setName(self, name):
        if not self.running:
            self.name = name

    def buzz(self):
        self.game.buzz(self.name)

