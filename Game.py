from copy import deepcopy

import Pyro.core
import Pyro.naming
from Pyro.errors import *

from PyQt4.QtCore import *

Pyro.config.PYRO_ONEWAY_THREADED = True	


class Game(Pyro.core.ObjBase):
    
    def __init__(self, server, parent = None):
        Pyro.core.ObjBase.__init__(self)
        self.server = server

    def canConnect(self, name):
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
        name = str(name)
        print 'Game: Connection from:', name
        player = Pyro.core.getProxyForURI('PYRONAME://' + name)
        ip = player.getIp()
        self.server.playerMutex.lock()
        score = self.server.players[name][3]
        status = self.server.players[name][2]
        self.server.players[name] = (player, player.getIp(), 'Waiting', score)
        self.server.scores[name] = [0]
        self.server.playerMutex.unlock()
        if status != 'Disconnected':
            self.server.playerConnected.emit((name, ip, 'Waiting', score))
            self.server.gamesToStart += 1
        else:
            self.server.playerReconnected.emit((name, ip, 'Waiting', score))

    def getPlayers(self):
        self.server.playerMutex.lock()
        players = [ (player[0], player[1][3]) for player in self.server.players.items() ]
        self.server.playerMutex.unlock()
        return players

    def getStatus(self, name):
        return self.server.players[name][2]

    def getScore(self, name):
        return self.server.players[name][3]
    
    def getResources(self):
        return deepcopy(self.server.resources)

    def getRound(self):
        return deepcopy(self.server.round)

    def getQuestion(self):
        return self.server.question

    def getUsedQuestions(self):
        return self.server.usedQuestions

    def getTemplate(self):
        return self.server.template

    def getWidth(self):
        return self.server.width

    def getHeight(self):
        return self.server.height

    def buzz(self, name):
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
        self.server.gamesToStart -= 1
        if self.server.gamesToStart == 0:
            print 'choosing player...'
            self.server.allGamesStarted.emit()

    def getScores(self):
        return deepcopy(self.server.scores)
