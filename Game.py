"""
This is the Game Pyro object. Multiple instances of this class can be active at
the same time retrieving information at the same time from the GameServer.
Game does not hold state as it is destroyed immediately after the remote method
invoked finishes execution.

It can only communicate to the rest of the 'Admin' program by calling emit on
its server's (GameServer) signals.

Players are represented by using a dictionary from player names to player tuples.
These tuples have a FIXED format::

  (uri, ip, status, score)
  [0]  [1]   [2]    [3]
"""
from copy import deepcopy

import Pyro.core
import Pyro.naming
from Pyro.errors import *

Pyro.config.PYRO_ONEWAY_THREADED = True

class Game(Pyro.core.ObjBase):
    """
    This class does not implement anything QObject based since it does not emit its own signals. That would have been too much of a hassle to create new connections every time such a temporary object is instantiated.
    Instead it uses the GameServer.
    """

    def __init__(self, server, parent = None):
        """
        @param server: the reference to the GameServer object (its Pyro server)
        @type server: GameServer
        """
        Pyro.core.ObjBase.__init__(self)
        self.server = server

    def canConnect(self, name):
        """
        When attempting to register with the server, a client first calls this method to see whether or not its name is reserved.

        If a player already exists in the server's L{GameServer.GameServer.players} dictionary, it will only allow connnections if the player has previously registered before the game started.

        This way, players cannot arbitrarily join the game.
        @param name: nickname a client is trying to register
        @type name: str
        @return: bool that says whether the login may proceed
        """
        name = str(name)
        self.server.playerMutex.lock()
        if self.server.loginEnabled:
            if name not in self.server.players:
                self.server.players[name] = (None, None, 'Waiting', 0)
                ans = True
            else:
                ans = False
        elif name in self.server.players and self.server.players[name][2] == 'Disconnected':
            ans = True
        else:
            ans = False
        self.server.playerMutex.unlock()
        return ans

    def connect(self, name):
        """
        This is the actual method where the login takes place.

        Each player already has an entry inside the  L{GameServer.GameServer.players} dictionary, but now the GameServer needs to know which URI to keep to be able to communicate with the Player Pyro objects.

        @param name: nickname a client is logging in with
        @type name: str
        """
        name = str(name)
        print 'Game: Connection from:', name
        player = Pyro.core.getProxyForURI('PYRONAME://' + str(hash(name)))
        ip = player.getIp()

        self.server.playerMutex.lock()
        score = self.server.players[name][3]
        status = self.server.players[name][2]
        self.server.players[name] = (player, ip, 'Waiting', score)
        self.server.scores[name] = ([0], None)
        self.server.playerMutex.unlock()

        if status != 'Disconnected':
            self.server.playerConnected.emit((name, ip, 'Waiting', score))
            self.server.gamesToStart += 1
        else:
            self.server.playerReconnected.emit((name, ip, 'Waiting', score))

    def getPlayers(self):
        """
        In order to display the player list in each table for the PlayerGui, the player list needs to be obtained.

        @return: list of player tuples containing their names and scores
        """
        self.server.playerMutex.lock()
        players = [ (player[0], player[1][3]) for player in self.server.players.items() ]
        self.server.playerMutex.unlock()
        return players

    def getStatus(self, name):
        """
        @return: the status for the player whose nickname is B{name} (str)
        """
        return self.server.players[name][2]

    def getScore(self, name):
        """
        @return: the score for the player whose nickname is B{name} (int)
        """
        return self.server.players[name][3]

    def getResources(self):
        """
        When parsing the .jeop files, there are also resources like images or html templates that need to be transferred to every player after login so that they're not downloaded when actually playing the game.

        Every file from the .jeop archive is returned in the resources array B{except for rules.json}, the file that contains the questions and answers.
        @return: a deep copy of the resources array
        """
        return deepcopy(self.server.resources)

    def getRound(self):
        """
        @return: a deep copy of the current round array
        """
        return deepcopy(self.server.round)

    def getQuestion(self):
        """
        @return: a deep copy of the current question
        """
        return deepcopy(self.server.question)

    def getUsedQuestions(self):
        """
        @return: a deep copy of the usedQuestions array (so that the buttons on the grid can be marked accordingly)
        """
        return deepcopy(self.server.usedQuestions)

    def getTemplate(self):
        """
        @return: string containing the html template that should be used to display the question
        """
        return self.server.template

    def getWidth(self):
        """
        @return: width of canvas on the server
        """
        return self.server.width

    def getHeight(self):
        """
        @return: height of canvas on the server
        """
        return self.server.height

    def buzz(self, name):
        """
        This function gets called when a player presses Buzz.

        The first player to call it obtains a lock on a mutex that ensures that only one player may answer at a time. After obtaining the lock:
          - the succesful player changes status to 'Answering'
          - every other player's buzzer is disabled
          - the rest of the program is notified to wait for an answer
        """
        self.server.buzzMutex.lock()
        if self.server.buzzed == False:
            self.server.buzzed = True
        else:
            self.server.buzzMutex.unlock()
            return
        self.server.buzzMutex.unlock()

        self.server.changeStatus(name, 'Answering')

        for player in self.server.players.items():
            try:
                player[1][0].disableBuzz()
            except (ConnectionClosedError, ProtocolError):
                self.server.changeStatus(player[0], 'Disconnected')

        self.server.playerBuzzed.emit(name)

    def gameStarted(self):
        """
        This function gets called whenever a client finished transfering the required resources and displaying the PlayerGui.
        When all of the clients are done, the game can start.
        """
        self.server.gamesToStart -= 1
        if self.server.gamesToStart == 0:
            self.server.allGamesStarted.emit()

    def getScores(self):
        """
        Possibly obsolete?
        @return: array of scores
        """
        return deepcopy(self.server.scores)

    ###################################
    def acceptQuestion(self, i):
        """
        This function gets called when the player selects a Question
        The admin is required to accept the Question (or not) for the actual question to be displayed to all players.
        """
        print 'question is', i
        self.server.accQuestion.emit(i)
