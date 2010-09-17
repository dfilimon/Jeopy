from PyQt4.QtGui import *
from PyQt4.QtCore import *

import Pyro.core

from PlayerServer import PlayerServer

class LoginDialog(QDialog):
    playerConnected = pyqtSignal()
    
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)
        self.setupGui()
        self.player = None
        
        self.connect(self.button, SIGNAL('clicked(bool)'), self.startPlayerServer)

    def startPlayerServer(self):
        name = str(self.lineEdit.text())
        if name == '':
            return
        if self.player == None:
            self.player = PlayerServer(None)
            print self.player.game.players
        if name in self.player.game.getPlayers():
             QMessageBox.warning(self, '', 'The selected nickname is taken.\nPlease choose a different one.', QMessageBox.Ok)
        else:
            self.player.setName(name)
            self.button.setDisabled(True)
            self.player.start()

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

def main():
    import sys
    app = QApplication(sys.argv)
    l = LoginDialog()
    l.show()
    app.exec_()

if __name__ == '__main__':
    main()
