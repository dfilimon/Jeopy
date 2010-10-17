import sys
from time import sleep

import Pyro.core
import Pyro.naming

from PyQt4.QtCore import *

class Server(QThread):
    """
       ***Signals common to both the GameServer and the PlayerServer***
    """
    serverStarted = pyqtSignal(str)

    """
    These signals trigger modifications in the gui
    """
    playerScoreChanged = pyqtSignal(tuple)
    """
    playerStatusChanged exists in both derived classes but behaves completely
    different. Do not try to add it here. PlayerServer emits a str whereas
    GameServer emits a tuple.
    """

    questionDisplayed = pyqtSignal(int)
    answerDisplayed = pyqtSignal()
    gridDisplayed = pyqtSignal()
    gameEnded = pyqtSignal()

    roundChanged = pyqtSignal()
    
    def __init__(self, gui, name, parent=None):
        super(Server, self).__init__(parent)
        self.daemon = None
        self.gui = gui
        self.name = name

    # When closing the app, its name must be unregistered from the NameServer
    def close(self):
        self.log('Server exitting')
        if self.daemon != None:
            self.daemon.shutdown(True)

    def run(self):
        self.setupSignals()
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

    def setupSignals(self):
        raise NotImplementedError('setupSignals is a virtual method and must be overridden')

    def setupGuiSignals(self):
        self.playerScoreChanged.connect(self.gui.getTable().updatePlayer)
        
        self.questionDisplayed.connect(self.gui.displayQuestion)
        self.answerDisplayed.connect(self.gui.displayAnswer)
        self.gridDisplayed.connect(self.gui.displayGrid)
        self.gameEnded.connect(self.gui.displayEndGame)
        
        self.roundChanged.connect(self.gui.updateGrid)
    
    def connectDaemon(self):
        raise NotImplementedError('connectDaemon is a virtual method and must be overridden')

    def log(self, message):
        print self.name + ': ' + message
        
