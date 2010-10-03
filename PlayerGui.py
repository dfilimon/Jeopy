#! /usr/bin/env python

import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PlayerServer import PlayerServer

from Gui import Gui
from PlayerTableWidget import PlayerTable

from LoginDialog import LoginDialog

class PlayerGui(Gui):
    buzzed = pyqtSignal()
    
    def __init__(self, parent = None):
        super(PlayerGui, self).__init__(parent)

        self.loginDialog = LoginDialog(self)
        self.loginDialog.show()
        self.player = None

    def startGame(self):
        self.player = self.loginDialog.player
        self.loginDialog.close()

        self.setupGui('Buzz', self.player.game.getWidth(), self.player.game.getHeight())
        self.show()

        for i in self.player.game.getUsedQuestions():
            self.getGrid().layout().itemAt(i).widget().setEnabled(False)
            
        self.player.setupGuiSignals()
        self.player.game.gameStarted()

    def getRound(self):
        return self.player.game.getRound()

    def getTemplate(self):
        return self.player.template

    def getTempPath(self):
        return self.player.tempPath

    def setupTable(self):
        table = PlayerTable(['Nickname', 'Score'], '')
        for player in self.player.game.getPlayers():
            table.addPlayer(player)
        return table

    def setupSignals(self):
        #self.getGrid().buttonClicked.connect(self.player.selectQuestion)
        self.getDisplayButton().clicked.connect(self.player.buzz)

    def playerHello(self):
        print 'player hello'

    def updateMessage(self, status):
        print 'updating', self.player.name, 'status to', status

        self.player.status = status
        if status == 'Waiting' or status == 'Muted':
            self.getLabel().setText('')
        elif status == 'Selecting':
            self.getLabel().setText('Select')
        elif status == 'Answering':
            self.getLabel().setText('Answer')

    def getQuestion(self):
        return self.player.game.getQuestion()

    def displayGrid(self):
        Gui.displayGrid(self)
        if self.player.game.getStatus(self.player.name) != 'Muted':
            self.getDisplayButton().setEnabled(True)
    
    def disableBuzz(self):
        self.getDisplayButton().setEnabled(False)

    def getScores(self):
        return self.player.game.getScores()

def main():
    import sys
    app = QApplication(sys.argv)
    gui = PlayerGui()
    app.exec_()

    if gui.player != None:
        gui.player.exit()

if __name__ == '__main__':
    main()
