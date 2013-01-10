"""
AdminDialog (PlayerAdminDialog) is the dialog used to view connecting players and
start the game.
Only displays the PlayerTable (in its admin 'view') and a 'ban' button that doesn't
do anything yet.
Its startGame signal triggers the actual start of the game.
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PlayerTableWidget import PlayerTable

class PlayerAdminDialog(QDialog):

	startGame = pyqtSignal()
	"""
	emitted when the game actually starts, connection in AdminGui.py
	"""

	def __init__(self, parent = None):
		super(PlayerAdminDialog, self).__init__(parent)
		self.setupGui()

	def setupGui(self):
		layout = QVBoxLayout()
		table = PlayerTable(['Nickname', 'IP', 'Status', 'Score'], 'ban')
		layout.addWidget(table)
		button = QPushButton('Start Game')
		button.clicked.connect(self.startGame.emit)
		layout.addWidget(button)
		self.setLayout(layout)

	def playerAdminTable(self):
		return self.layout().itemAt(0).widget()

	def addPlayer(self, player):
		self.playerAdminTable().addPlayer(player)
		self.adjustSize()
		self.layout().activate()

