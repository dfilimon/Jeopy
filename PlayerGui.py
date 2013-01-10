#! /usr/bin/env python

"""
PlayerGui is the main player interface class. It also launches LoginDialog to get
a name. The main gui actually appears after startGame is called from the server.
This class must be instantiated after having chosen a jeop game file. Otherwise,
it will silently fail.
"""
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from Gui import Gui
from PlayerServer import PlayerServer

from PlayerTableWidget import PlayerTable

from LoginDialog import LoginDialog

class PlayerGui(Gui):
	buzzed = pyqtSignal()

	"""
	   ***REIMPLEMENTED METHODS FROM BASECLASS***
	   These work similarly to the ones in AdminGui. For more information, check
	   those.
	"""
	def __init__(self, parent = None):
		super(PlayerGui, self).__init__(parent)
		self.player = None
		self.loginDialog = LoginDialog(self)
		self.loginDialog.show()

	def setupGui(self, buttonText, width, height):
		Gui.setupGui(self, buttonText, width, height)
		self.setLabelText(self.player.name)

	def startGame(self):
		self.player = self.loginDialog.player
		self.loginDialog.close()

		self.setupGui('Buzz', self.player.game.getWidth(), self.player.game.getHeight())
		for i in self.player.game.getUsedQuestions():
			self.getGridButton(i).setEnabled(False)

		self.show()
		self.gameStarted.emit()
		self.player.game.gameStarted()

	def setupTable(self):
		table = PlayerTable(['Nickname', 'Score'], '')
		for player in self.player.game.getPlayers():
			table.addPlayer(player)
		return table

	def setupSignals(self):
		self.gameStarted.connect(self.player.setupGuiSignals)
		self.getDisplayButton().clicked.connect(self.player.buzz)

	def displayQuestion(self, i):
		Gui.displayQuestion(self, i)
		if self.player.game.getStatus(self.player.name) != 'Muted':
			self.getDisplayButton().setEnabled(True)

	def getRound(self):
		return self.player.game.getRound()

	def getQuestion(self):
		return self.player.game.getQuestion()

	def getTemplate(self):
		return self.player.template

	def getTempPath(self):
		return self.player.tempPath

	def getScores(self):
		return self.player.game.getScores()

	"""
	The player's status is displayed above the PlayerTable. {Waiting,Selecting,
	Answering} -> [:-3]
	"""
	def updateStatus(self, status):
		self.log('Updating ' + self.player.name + ' status to ' + status)

		self.player.status = status
		if status == 'Muted':
			self.setLabelText('Muted')
		else:
			self.setLabelText(status[:-3])

	def disableBuzz(self):
		self.getDisplayButton().setEnabled(False)

def main():
	app = QApplication(sys.argv)
	gui = PlayerGui()
	app.exec_()

	if gui.player != None:
		gui.deleteTempFiles()
		gui.player.close()

if __name__ == '__main__':
	main()

