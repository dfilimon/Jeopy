from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PlayerTableWidget import PlayerTable

class PlayerAdminDialog(QDialog):

    startGame = pyqtSignal()

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
        #self.setMinimumWidth(550)

    def playerAdminTable(self):
        return self.layout().itemAt(0).widget()

    def addPlayer(self, player):
        self.playerAdminTable().addPlayer(player)
        self.adjustSize()
        self.layout().activate()
        
