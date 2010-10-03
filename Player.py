import os, tempfile

import Pyro.core
import Pyro.naming

from PyQt4.QtCore import *

class Player(Pyro.core.ObjBase):
    
    def __init__(self, server, parent = None):
        Pyro.core.ObjBase.__init__(self)
        self.server = server

    def loadResources(self):
        self.server.template = self.server.game.getTemplate()
        self.server.resources = self.server.game.getResources()
        self.server.tempPath = tempfile.mkdtemp()
        for resource in self.server.resources.items():
            print 'Player:', self.server.name, 'transferring:', resource[0]
            f = open(self.server.tempPath + '/' + resource[0], 'w')
            f.write(resource[1])
            f.close()

    def getName(self):
        return self.server.name

    def getIp(self):
        return self.server.ip

    def startGame(self):
        self.server.gameStarted.emit()

    def displayQuestion(self, i):
        self.server.questionDisplayed.emit(i)

    def displayAnswer(self):
        self.server.answerDisplayed.emit()

    def disableBuzz(self):
        self.server.buzzDisabled.emit()

    def displayGrid(self):
        self.server.gridDisplayed.emit()

    def displayPlot(self):
        self.server.plotDisplayed.emit()

    def changeStatus(self, status):
        print self.server.name, 'changing status to', status
        self.server.playerStatusChanged.emit(status)
        if status == 'Muted':
            self.server.buzzDisabled.emit()

    def changeScore(self, name, score):
        self.server.playerScoreChanged.emit((name, score))

    def nextRound(self):
        self.server.roundChanged.emit()

