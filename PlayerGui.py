import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PlayerServer import *

from ButtonGridWidget import ButtonGrid
from QuestionDisplayWidget import QuestionDisplay
from PlayerTableWidget import PlayerTable

from LoginDialog import LoginDialog

class PlayerGui(QMainWindow):
    
    def __init__(self, parent = None):
        super(PlayerGui, self).__init__(parent)

        loginDialog = LoginDialog(self)
        loginDialog.show()

    def startGame(self, player):
        self.player = player
        self.setupGui()
        self.show()

    def setupGui():
        pass

def main():
    import sys
    app = QApplication(sys.argv)
    gui = PlayerGui()
    app.exec_()

if __name__ == '__main__':
    main()
