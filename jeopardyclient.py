import Pyro.core
import sys, time

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import playerserver

class Client(QDialog):
    def __init__(self, parent = None):
        super(Client, self).__init__(parent)

        self.name = ''

        self.nameEdit = QLineEdit()
        self.loginButton = QPushButton('Login')
        self.greetButton = QPushButton('Greet')

        layout = QHBoxLayout()
        layout.addWidget(self.nameEdit)
        layout.addWidget(self.loginButton)
        layout.addWidget(self.greetButton)

        self.setLayout(layout)

        self.connected = False
        self.connect(self.loginButton, SIGNAL('clicked(bool)'), self.login)

        self.connect(self.greetButton, SIGNAL('clicked(bool)'), self.greet)

    def login(self):
        if self.connected == True:
            return
        
        if self.nameEdit.text() != self.name:
            self.name = self.nameEdit.text()
            
        if self.name != '':
            self.server = playerserver.PlayerServerThread(str(self.name))
            self.server.start()
            self.connect(self.server, SIGNAL('serverStarted'), self.registerName)

    def registerName(self):
        self.player = Pyro.core.getProxyForURI('PYRONAME://' + str(self.name))
        self.player.greet()
        self.connected = True
        self.connect(self, SIGNAL('sayHello'), self.server.sayHello)
            
    def greet(self):
        print 'hello'
        if self.connected == True:
            self.player.greet()
            self.emit(SIGNAL('sayHello'))
            
    def __del__(self):
        try:
            self.server.exit()
        except:
            pass
    
def main(): 
    app = QApplication(sys.argv)
    client = Client()
    client.show()
    app.exec_()

if __name__ == '__main__':
    main()
