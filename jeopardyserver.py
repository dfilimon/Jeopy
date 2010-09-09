#!/usr/bin/env python

# Jeopardy Server

import sys
import logging

#from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *

import Pyro.core
import Pyro.naming

import jeopardyquestion # game question class

class Game(Pyro.core.ObjBase):
    
    def __init__(self):
        self.buzzed = False
        Pyro.core.ObjBase.__init__(self)
        
    def loadGameRules(self, gameRules):
        pass

    def sayHi(self, name):
        print 'Hello, evil minion', name
        return 'This is your overloard speaking'

    def buzz(self, name):
        if self.buzzed == False:
            print name, 'buzzed first!'
            self.buzzed = True
            return 'answer!'
        else:
            print name, 'is late!'
            return 'silence!'

def main():
    #logging.basicConfig(level = logging.INFO)
    
    #logging.info('Starting Jeopardy Server')

    Pyro.core.initServer()
    ns = Pyro.naming.NameServerLocator().getNS()
    
    daemon = Pyro.core.Daemon()
    daemon.useNameServer(ns)
    uri = daemon.connect(Game(), 'jeopardy')

    #logging.info('The daemon runs on port:', daemon.port)
    #logging.info('The object\'s URI is:', uri)
    print 'The daemon runs on port:', daemon.port
    print 'The game\'s URI is:', uri    

    daemon.requestLoop()

if __name__ == '__main__':
    main()
