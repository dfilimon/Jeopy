#! /usr/bin/env python

"""
AdminGui is the administrative interface's main class. It provides game file
selection, validation, player management and question selection.
This class must be instantiated before any player connection may be attempted.
"""
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from RuleLoader import validateFile

from Gui import Gui
from GameServer import GameServer

from PlayerTableWidget import PlayerTable

from PlayerAdminDialog import PlayerAdminDialog

class AdminGui(Gui):
    """
    Signals are used to communicate with the GameServer, which is in a
    different thread. Any instance where a GameServer method is called
    directly is a _bug_. Please report it.
    """    
    answerShown = pyqtSignal()
    answerChecked = pyqtSignal(str, bool)

    mutePlayers = pyqtSignal(list)
    unmutePlayers = pyqtSignal(list)
    
    def __init__(self, parent=None):    
        super(AdminGui, self).__init__(parent)
        self.game = GameServer(self, 'jeopardy')

        self.loadRules()

        """
        Setup the player table, and wait for players to login before
        the game may be started.
        """
        self.playerAdmin = PlayerAdminDialog(self)        
        self.playerAdmin.startGame.connect(self.startGame)
        self.playerAdmin.show() # does not block thread, __init__ continues
        
        # starts the GameServer thread
        self.game.start()
        
        # prepare to tell the time elapsed since the game started
        self.time = QTime(0, 0, 0)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.displayTime)

    """
    loadRules is where the user selects a game file (*.jeop) and where it is
    validated by the RuleLoader module. After (if) this function finishes, the
    GameServer object, self.game will contain the rules read from the file.
    The RuleLoader may be used on its own to test the validity of .jeop files.
    """
    def loadRules(self): 
        fileName = ''
        while fileName == '':  
            fileName = QFileDialog.getOpenFileName(self,
                                                   'Select a Jeopardy game file',
                                                   'example.jeop',
                                                   'Jeopardy game files (*.jeop)')
            if fileName == '':
                sys.exit()
            self.log('Validating ' + fileName)
            
            # validateFile is the actual function from RuleLoader that is called
            if validateFile(self.game, fileName) == False:
                ans = QMessageBox.warning(self, '',
                                          'The selected game file is invalid.\nPlease choose a different one.',
                                          QMessageBox.Ok | QMessageBox.Cancel)
                if ans == QMessageBox.Cancel:
                    sys.exit()
                fileName = ''
            else:
                self.log('Loaded ' + fileName)

    """
    The actual game ui is set up and the AdminGui instructs the GameServer to
    startGames for all players
    """
    def startGame(self):
        self.playerAdmin.close()
        self.game.loginEnabled = False
        
        self.game.nextRound()
        self.setupGui('Show Answer', self.game.width, self.game.height)
        self.getDisplayButton().clicked.connect(self.game.showAnswer)
        self.timer.start(1000)

        self.show()
        self.gameStarted.emit()

    """
    Virtual methods required in Gui implemented here. In this case, all the data
    is in the GameServer. No mutexes are used because GameServer cannot ever modify
    these fields at the same time AdminGui reads them.
    """
    def getRound(self):
        return self.game.round

    def getQuestion(self):
        return self.game.question

    def getTempPath(self):
        return self.game.tempPath

    def getTemplate(self):
        return self.game.template

    def getScores(self):
        return self.game.scores

    """
    Custom table used in the AdminGui.
    Players can be muted and their Status is displayed. Use it to determine who
    can select a question, who can answer and who is disconnected.
    """
    def setupTable(self):
        table = PlayerTable(['Nickname', 'IP', 'Status', 'Score'], 'mute')
        for player in self.game.players.items():
            table.addPlayer((player[0], player[1][1], player[1][2], player[1][3]))
        return table

    """
    Communication between AdminGui and GameServer is setup here. The actual logic
    behind most operations pertaining players is in the GameServer.
    - player Mute/Unmute, from table buttons
    - answerChecked, for score modification
    - showing the answer to everyone from QuestionDisplay button;
      note: this signal is not always connected as that button is also used
      for progressing to the next question in addition to showing the answer
    - question selection from ButtonGrid
    """
    def setupSignals(self):
        self.gameStarted.connect(self.game.startGame)
        self.getTable().playersMuted.connect(self.game.mutePlayers)
        self.getTable().playersUnmuted.connect(self.game.unmutePlayers)
        self.answerChecked.connect(self.game.checkAnswer)
        self.getDisplay().buttonClicked.connect(self.game.showAnswer)
        self.getGrid().buttonClicked.connect(self.game.selectQuestion)
        

    """
    The admin user decides whether a question is correct or not regardless of the
    actual answer's formulation.
    """
    def playerBuzzed(self, name):
         ans = QMessageBox.information(self, '', 'Player ' + name + ' is answering.\nIs the answer correct?', QMessageBox.Yes | QMessageBox.No)
         if ans == QMessageBox.Yes:
             add = True
         else:
             add = False
         self.answerChecked.emit(name, add)

    # refreshes the timer every second
    def displayTime(self):
        self.time = self.time.addSecs(1)
        self.getLabel().setText(self.time.toString())

    """
    Same functions as in Gui class, but also handling the double-use button
    """
    def displayQuestion(self, i):
        Gui.displayQuestion(self, i)
        self.displayShowAnswerButton()
        
    def displayAnswer(self):
        Gui.displayAnswer(self)
        self.displayNextQuestionButton()

    def displayNextQuestionButton(self):
        self.getDisplayButton().clicked.disconnect()
        self.getDisplayButton().setText('Next Question')
        self.getDisplayButton().clicked.connect(self.game.nextQuestion)

    def displayShowAnswerButton(self):
        self.getDisplayButton().clicked.disconnect()
        self.getDisplayButton().setText('Show Answer')
        self.getDisplayButton().clicked.connect(self.game.showAnswer)
        
    """
    Since the ButtonGrid is used for question selection, when a new one is created,
    because of a change of round, the buttonClicked signal must be reconnected.
    """
    def updateGrid(self):
        self.getGrid().buttonClicked.disconnect()
        Gui.updateGrid(self)
        self.getGrid().buttonClicked.connect(self.game.selectQuestion)

    """
    The AdminGui can also save the scores in addition to displaying them.
    """
    def displayEndGame(self):
        self.getTable().hideButtons()
        Gui.displayEndGame(self)

    def displayPlot(self, path):
        Gui.displayPlot(self, path)
        
        w = QPushButton('Save scores as PNG')
        w.clicked.connect(self.saveScoresPng)
        self.layout().addWidget(w, 2, 0)
        
        w = QPushButton('Save scores as text file')
        w.clicked.connect(self.saveScoresText)
        self.layout().addWidget(w, 2, 1)

    def saveScoresText(self):
        fileName = QFileDialog.getSaveFileName(self, 'Save Scores', 'scores.txt', 'Text files (*.txt)')
        fp = open(fileName, 'w')
        for player in self.game.players.items():
            fp.write(player[0] + '\t' + str(player[1][3]) + '\n')
        fp.close()

    def saveScoresPng(self):
        fileName = QFileDialog.getSaveFileName(self, 'Save Scores', 'scores.png', 'Images (*.png)')
        self.pixmap.save(fileName)
        
    
def main():
    app = QApplication(sys.argv)
    gui = AdminGui()    
    app.exec_()

    if gui.game != None:
        gui.deleteTempFiles()
        gui.game.close()
        
if __name__ == '__main__':
    main()

