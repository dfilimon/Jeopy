"""
Small dialog the player sees when starting the PlayerGui.
It only allows login. The actual start of the game is determined by the GameServer.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *

import Pyro.core

from PlayerServer import PlayerServer

class LoginDialog(QDialog):
	gameStarted = pyqtSignal((type(PlayerServer)))
	playerConnected = pyqtSignal()

	def __init__(self, parent=None):
		super(LoginDialog, self).__init__(parent)
		self.setupGui()
		self.gui = parent
		self.player = PlayerServer(self.gui, None)

		self.button.clicked.connect(self.login)
		self.player.playerConnected.connect(self.disableLogin)

	def login(self):
		"""
		Enable login with the selected name.
		Fix: Pop up message saying that the lineEdit is empty!
		"""
		name = str(self.lineEdit.text())
		if name == '':
			QMessageBox.warning(self, '', 'Please enter a name!', QMessageBox.Ok)
			return

		canConnect = self.player.game.canConnect(name)

		if canConnect == False or name == 'jeopardy':
			 QMessageBox.warning(self, '', 'The selected nickname is taken.\nPlease choose a different one.', QMessageBox.Ok)
		else:
			self.player.setName(name)
			self.player.start()

	def disableLogin(self):
		self.button.setEnabled(False)

	def setupGui(self):
		layout = QHBoxLayout()

		w = QLabel()
		w.setText('Nickname:')
		layout.addWidget(w)

		self.lineEdit = QLineEdit()
		layout.addWidget(self.lineEdit)

		self.button = QPushButton()
		self.button.setText('Login')
		layout.addWidget(self.button)

		self.setLayout(layout)
