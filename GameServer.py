"""
GameServer is the class responsible for spawning Pyro threads of the Game object.
Game objects themselves have an extremely limited lifetime as instances are
created whenever needed. That means that any data that needs to be stored must be
somewhere else. In this case, the Server object.
The GameServer is also responsible of relaying messages from the Game Pyro object
that is exposed to clients to the AdminGui. This works through QThreads.
"""
import sys, random
from copy import deepcopy

import Pyro.core
import Pyro.naming
from Pyro.errors import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Server import Server
from Game import Game

from PyQt4.QtGui import QColor

class GameServer(Server):
    """
    Signals used to communicate with Gui. Do not update interface elements, or
    perform non reentrant operations:
    calling self.gui.displayGrid() can possibly cause a SIGSEGV
    use self.gridDisplayed.emit() since inter-thread communication is sure to work
    """
    playerConnected = pyqtSignal(tuple)
    playerReconnected = pyqtSignal(tuple)
    playerStatusChanged = pyqtSignal(tuple)

    playerBuzzed = pyqtSignal(str)
    questionSelected = pyqtSignal(int)

    labelTextSet = pyqtSignal(str)
    allGamesStarted = pyqtSignal()

    """
    Concurrent access to the player table for modification (at login) could lead
    to a corrupt data structure. That's why a mutex must be obtained before
    modifying it.

    As for buzzing, since only one player can be the first to buzz, a lock is
    obtained immediately after the first buzz was recieved to prevent having
    multiple people answering at the same time.
    """
    playerMutex = QMutex()
    buzzMutex = QMutex()

    """
       ***REIMPLEMENTED METHODS FROM BASECLASS***
    """
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
        self.usedQuestions = set()

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

    """
       ***GAME FUNCTIONS*** 
    """
    """
    Methods for starting a new game.
    Gui signals are not connected when this function is called.
    """
    def startGame(self):
        for name in self.players.keys():
            self.startPlayerGame((name, 0))
        self.setupGuiSignals()

    """
    Starting a player's client gui means:
    - sending over the resources needed for the questions (image files, html templates, etc.)
    - actually calling a startGame method so that the guis are loaded
    """
    def startPlayerGame(self, player):
        name = player[0]
        try:
            self.players[name][0].loadResources()
            self.players[name][0].startGame()
        except (ConnectionClosedError, ProtocolError):
            self.changeStatus(name, 'Disconnected')

    """
    Without setting loginEnabled True, nobody is allowed to log in, unless they
    are marked as 'Disconnected'.
    """
    def enableLogin(self):
        self.log('Login enabled')
        self.loginEnabled = True


    """
    When no answer was given last turn or the answer given was false, a player
    is chosen at random to select the next question.
    Muted and disconnected players don't count.
    """
    def choosePlayer(self):
        numActivePlayers = len(self.players)
        for player in self.players.values():
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

    """
    When a question is selected (by the admin, requested by a player)
    - it's loaded into the question variable to not do any more lookups
    - the game prepares to recieve a buzz
    - player statuses are changed to Waiting
    - player guis are signaled to display the ButtonGrid
    """
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
   
    """
    Once the admin has validated the answer through the messagebox in the AdminGui
    this function, that calculates the new score is called.
    Afterwards, the correct answer is displayed.
    """
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

    """
    Displays the answer to all players and updates the scores array.
    The scores array is required to draw the final plot at the end of the game.
    """
    def showAnswer(self):
        for player in self.players.items():
            try:
                player[1][0].disableBuzz()
                player[1][0].displayAnswer()
            except (ConnectionClosedError, ProtocolError):
                self.changeStatus(player[0], 'Disconnected')
                
            self.scores[player[0]][0].append(player[1][3])

        # used to be self.gui.displayAnswer()... I wonder if this caused the SIGSEGV
        self.answerDisplayed.emit()

    """
    The game continues by waiting for another question to be selected.
    First,
    we must find out if there are any more questions this round, or if there are
    any more questions at all.
    Second,
    a player must be chosen to select a question - if the last answer was correct,
    then the player who gave that answer gets to pick, otherwise, a player is
    chosen at random.
    Third,
    the players are signaled to display the ButtonGrids and the AdminGui itself
    displays its grid.
    """
    def nextQuestion(self):
        if len(self.usedQuestions) == self.numQuestions:
            if not self.nextRound():
                return
            
        if self.selectingPlayer == '' or self.players[self.selectingPlayer][2] == 'Disconnected':
            self.choosePlayer()
        else:
            self.changeStatus(self.selectingPlayer, 'Selecting')
            self.selectingPlayer = ''
            
        for player in self.players.items():
            try:
                player[1][0].displayGrid()
            except (ConnectionClosedError, ProtocolError):
                self.changeStatus(player[0], 'Disconnected')

        self.gridDisplayed.emit()

    """
    When progressing to the next round:
    - the round variable of the GameServer needs to be updated
    - the usedQuestions array needs to be emptied
    - the numQuestions needs to be recalculated
    - gui events need to be trigerred to replace the ButtonGrid with a new one
    """
    def nextRound(self):
        self.roundNum += 1
        
        if self.roundNum >= self.numRounds:
            self.endGame()
            return False

        # updating game state
        self.round = self.rules['rounds'][self.roundNum]
        self.usedQuestions = set()
        self.numQuestions = 0
        for c in self.round['categories']:
            self.numQuestions += len(c['questions'])

        # trigerring gui events (Player.nextRound emits a signal)
        if self.roundNum > 0:
            for player in self.players.items():
                try:
                    player[1][0].nextRound()
                except (ConnectionClosedError, ProtocolError):
                    self.changeStatus(player[0], 'Disconnected')
            self.roundChanged.emit()
        return True

    """
    At the end of the game, when there are no more questions and no more rounds,
    this function gets called to trigger the drawing of the score plots.
    Also, assigns a color to each player in the game.
    """
    def endGame(self):
        hue = 0
        hueInc = 360 / len(self.scores.items())
        
        for e in self.scores.items():
            color = QColor()
            color.setHsv(hue, 255, 240)
            hue += hueInc - 1
            self.scores[e[0]] = (e[1][0], color.getRgbF())

        # actually ending the game here...
        for player in self.players.values():
                player[0].endGame()
        self.gameEnded.emit()

    """
       ***UTILITY FUNCTIONS***
    """
    """
    When selecting a question through the ButtonGrid, the position of the item in
    the grid is emitted. That is not however the actual number of the question.
    From that index, category and question number can be determined.
    This function supports categories with a different number of questions.
    """
    def toLineCol(self, round, index):
        n = len(round['categories'])
        maxIndex = 0
        for i in range(n):
            maxIndex += len(round['categories'][i]['questions']) + 1
            if index <= maxIndex:
                break
        j = index - (maxIndex - len(round['categories'][i]['questions']))
        return (i, j)

    """
    Players are muted/unmuted through these functions as long as the players in
    the names array are not Selecting. A Selecting player cannot be muted.
    """
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

    

    """
    Changing a player's status or score works in pretty much the same way.
    The player entry in the players table is copied and the required field is
    modified. The entry is then put back in the dictionary and the proper signals
    are emitted.
    """
    def changeStatus(self, name, status):
        player = self.players[name]
        self.players[name] = (player[0], player[1], status, player[3])
        self.playerStatusChanged.emit((name, player[1], status, player[3]))
        if status != 'Disconnected':
            try:
                player[0].changeStatus(status)
            except (ConnectionClosedError, ProtocolError):
                self.changeStatus(name, 'Disconnected')
           
    def changeScore(self, name, score):
        player = self.players[name]
        self.players[name] = (player[0], player[1], player[2], score)
        self.playerScoreChanged.emit((name, player[1], player[2], score))
        for player in self.players.items():
            try:
                player[1][0].changeScore(name, score)
            except (ConnectionClosedError, ProtocolError):
                self.changeStatus(player[0], 'Disconnected')

    
