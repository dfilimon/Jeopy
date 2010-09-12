from PyQt4.QtGui import *
from PyQt4.QtCore import *

import Pyro.core

import PlayerServer

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        super(LoginDialog, self).__init__(parent)

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

        self.connect(self.button, SIGNAL('clicked(bool)'), self.startPlayerServer)

    def startPlayerServer(self):
        if self.lineEdit.text() != '':
            print str( self.lineEdit.text() )
            #self.player = PlayerServer(self.lineEdit.text().toStr())
            #self.connect(self.player, SIGNAL('serverStarted'), self.loadMainWindow)
            self.button.setDisabled(True)

    def loadMainWindow(self):
        pass

def main():
    import sys
    app = QApplication(sys.argv)
    l = LoginDialog()
    l.show()
    app.exec_()

if __name__ == '__main__':
    main()
