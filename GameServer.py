import sys
from time import sleep

import Pyro.core
import Pyro.naming

from PyQt4.QtCore import *

from Server import Server
from Game import Game

class GameServer(Server):

    playerConnected = pyqtSignal(QString)
    playerMutex = QMutex()
    
    def __init__(self, gui, name, parent = None):
        Server.__init__(self, gui, name)
        
        self.rules = ''
        self.resources = []
        self.type = ''
        self.numRounds = 0
        self.numCategories = []
        self.numQuestions = []
        self.loginEnabled = False
        self.players = {}

        self.round = -1
        self.usedQuestions = None

    def connectSignals(self):
        self.playerConnected.connect(self.gui.adminView.insertItem)
        self.serverStarted.connect(self.gui.enableLogin)
        self.playerConnected.connect(self.gui.hello)

    def connectDaemon(self):
        self.uri = self.daemon.connect(Game(self), self.name)

    def getPlayers(self):
        return self.players

    def greet(self, name):
        #print 'GameServer:', name, 'connected'
        print self.players

"""
    def connect(self, name):
        if self.loginEnabled:
            print 'GameServer: Connection from:', name
            self.players[name] = (0,  Pyro.core.getProxyForURI('PYRONAME://' + name))
            print self.players[name]
            #self.players[name][1].greet()
            print 'Game: hello', self.gui, self, self.server
            self.playerConnected.emit(name)
            print self.rules
            #self.gui.hello(name)
            #self.playerGreet.emit(name)
"""

    
"""
def main():
    app = QCoreApplication(sys.argv)

    server.start()
    for i in range(1, 10):
        print 'Testing...', i
    #server.join()
    
    #server.terminate()
    key = 'a'
    while key != 'x':
        key = raw_input('Press \'x\' to terminate Player Server Thread\n')
        if key == 'x':
            server.exit()
        sleep(1)
    #print 'Server thread finished'
    sys.exit()
    app.exec_()

if __name__ == '__main__':
    main()
"""
