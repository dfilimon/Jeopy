import sys, random
from time import sleep
from copy import deepcopy

import Pyro.core
import Pyro.naming
from Pyro.errors import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Server import Server
from Game import Game

Pyro.config.PYRO_ONEWAY_THREADED = True	

class GameServer(Server):

    playerConnected = pyqtSignal(tuple)
    playerReconnected = pyqtSignal(tuple)
    playerStatusChanged = pyqtSignal(tuple)

    playerBuzzed = pyqtSignal(str)
    questionSelected = pyqtSignal(int)

    labelTextSet = pyqtSignal(str)
    allGamesStarted = pyqtSignal()
    
    playerMutex = QMutex()
    buzzMutex = QMutex()
    
    def __init__(self, gui, name, parent = None):
        Server.__init__(self, gui, name)
        
        self.rules = ''
        self.resources = []
        self.type = ''
        self.numRounds = 0
        self.numCategories = []
        self.numQuestions = []
        self.loginEnabled = True
        self.players = {}
        self.scores = {}
        self.gamesToStart = 0

        self.selectingPlayer = ''

        self.roundNum = -1
        self.pixmap = None
        self.usedQuestions = set()

    """
    Without setting loginEnabled True, nobody is allowed to log in, unless they
    are marked as 'Disconnected'.
    """
    def enableLogin(self):
        self.log('Login enabled')
        self.loginEnabled = True

    def setupSignals(self):
        self.serverStarted.connect(self.enableLogin)
        self.playerConnected.connect(self.gui.playerAdmin.addPlayer)
        self.allGamesStarted.connect(self.choosePlayer)

    def setupGuiSignals(self):
        Server.setupGuiSignals(self)
        self.playerReconnected.connect(self.gui.getTable().updatePlayer)
        self.playerReconnected.connect(self.startPlayerGame) 
        self.playerStatusChanged.connect(self.gui.getTable().updatePlayer)

        self.playerBuzzed.connect(self.gui.playerBuzzed)
        self.questionSelected.connect(self.gui.displayQuestion)

        self.labelTextSet.connect(self.gui.setLabelText)

    def connectDaemon(self):
        self.uri = self.daemon.connect(Game(self), self.name)
        
    def endGame(self):
        for player in self.players.values():
                player[0].endGame()
        self.gameEnded.emit()
    
    def nextRound(self):
        self.roundNum += 1
        
        if self.roundNum >= self.numRounds:
            self.endGame()
            return False
        self.round = self.rules['rounds'][self.roundNum]

        self.usedQuestions = set()
        self.numQuestions = 0
        for c in self.round['categories']:
            self.numQuestions += len(c['questions'])
       
        if self.roundNum > 0:
            for player in self.players.items():
                try:
                    player[1][0].nextRound()
                except (ConnectionClosedError, ProtocolError):
                    self.changeStatus(player[0], 'Disconnected')
            self.roundChanged.emit()
        return True

    def startGame(self):
        for name in self.players.keys():
            self.startPlayerGame((name, 0))
        self.setupGuiSignals()

    def startPlayerGame(self, player):
        name = player[0]
        print name, player
        try:
            self.players[name][0].loadResources()
            self.players[name][0].startGame()
        except (ConnectionClosedError, ProtocolError):
            self.changeStatus(name, 'Disconnected')
    
    def choosePlayer(self):
        numActivePlayers = len(self.players)
        for player in self.players.values():
            print player
            if player[2] == 'Muted' or player[2] == 'Disconnected':
                numActivePlayers -= 1
        n = random.randint(0, numActivePlayers - 1)
        for player in self.players.items():
            if player[1][2] == 'Muted' or player[1][2] == 'Disconnected':
                continue
            if n == 0:
                self.changeStatus(player[0], 'Selecting')
                break
            else:
                n -= 1

    def checkAnswer(self, name, ans):
        name = str(name)
        player = self.players[name]
       
        score = player[3]
        if ans == True:
            score += self.question['value']
            self.selectingPlayer = name
            self.changeScore(name, score)
        else:
            score -= self.question['value']
            self.selectingPlayer = ''
            self.changeScore(name, score)
        self.changeStatus(name, 'Waiting')
                
        self.showAnswer()

    def showAnswer(self):
        for player in self.players.items():
            try:
                player[1][0].disableBuzz()
                player[1][0].displayAnswer()
            except (ConnectionClosedError, ProtocolError):
                self.changeStatus(player[0], 'Disconnected')
                
            self.scores[player[0]].append(player[1][3])
            
        self.gui.displayAnswer()

    def mutePlayers(self, names):
        for name in names:
            if name == self.selectingPlayer:
                continue
            if name in self.players.keys() and self.players[name][2] == 'Waiting':
                self.changeStatus(name, 'Muted')

    def unmutePlayers(self, names):
        for name in names:
            if name in self.players.keys() and self.players[name][2] == 'Muted':
                self.changeStatus(name, 'Waiting')

    def nextQuestion(self):
        if self.selectingPlayer == '' or self.players[self.selectingPlayer][2] == 'Disconnected':
            self.choosePlayer()
        else:
            self.changeStatus(self.selectingPlayer, 'Selecting')
            self.selectingPlayer = ''
            
        if len(self.usedQuestions) == self.numQuestions:
            if not self.nextRound():
                return
        for player in self.players.items():
            try:
                player[1][0].displayGrid()
            except (ConnectionClosedError, ProtocolError):
                self.changeStatus(player[0], 'Disconnected')
        
        self.gui.displayGrid()

    def changeStatus(self, name, status):
        print 'server', name, 'changing status to', status
        
        player = self.players[name]
        self.players[name] = (player[0], player[1], status, player[3])
        self.playerStatusChanged.emit((name, player[1], status, player[3]))
        if status != 'Disconnected':
            try:
                player[0].changeStatus(status)
            except (ConnectionClosedError, ProtocolError):
                self.changeStatus(name, 'Disconnected')
            
        print self.players

    def changeScore(self, name, score):
        player = self.players[name]
        self.players[name] = (player[0], player[1], player[2], score)
        self.playerScoreChanged.emit((name, player[1], player[2], score))
        for player in self.players.items():
            try:
                player[1][0].changeScore(name, score)
            except (ConnectionClosedError, ProtocolError):
                self.changeStatus(player[0], 'Disconnected')
            

    def toLineCol(self, round, index):
        print round, index
        n = len(round['categories'])
        maxIndex = 0
        for i in range(n):
            maxIndex += len(round['categories'][i]['questions']) + 1
            if index <= maxIndex:
                break
        j = index - (maxIndex - len(round['categories'][i]['questions']))
        return (i, j)


    def selectQuestion(self, i):
        (c, q) = self.toLineCol(self.round, i)
        
        category = self.round['categories'][c]
        self.question = deepcopy(category['questions'][q])
        self.question['category'] = category['title']
        self.buzzed = False

        self.usedQuestions.add(i)
        
        for player in self.players.items():
            if player[1][2] == 'Selecting':
                self.changeStatus(player[0], 'Waiting')
            try:
                player[1][0].displayQuestion(i)
            except (ConnectionClosedError, ProtocolError):
                self.changeStatus(player[0], 'Disconnected')

        self.questionSelected.emit(i)
