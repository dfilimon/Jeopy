import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class PlayerAdminView(QWidget):
    gameStarted = pyqtSignal()
    
    def __init__(self, parent = None):
        super(PlayerAdminView, self).__init__(parent)

        layout = QGridLayout()
        layout.addWidget(QLabel('Connected players:'), 0, 0, 1, 2)
        listView = QListWidget()
        #listView.addColumn('Nickname')
        #listView.addColumn('Connected')
        #listView.addColumn('Ban')
        listView.insertItem(0, QListWidgetItem('one'))
        listView.insertItem(0, QListWidgetItem('two'))
        listView.insertItem(0, QListWidgetItem('three'))
        listView.setSelectionMode(QAbstractItemView.ExtendedSelection)

        layout.addWidget(listView, 1, 0, 1, 2)
        layout.addWidget(QPushButton('Ban'), 2, 0)
        layout.addWidget(QPushButton('Start Game'), 2, 1)
        self.setLayout(layout)
        self.connect(self.layout().itemAtPosition(2, 0).widget(), SIGNAL('clicked(bool)'), self.printSelected)

        self.layout().itemAtPosition(2, 1).widget().clicked.connect(self.gameStarted.emit)

    def insertItem(self, name):
        print name
        self.layout().itemAtPosition(1, 0).widget().insertItem(0, name)
        
    def printSelected(self):
        print 'hello'
        print [x.text() for x in self.layout().itemAtPosition(1, 0).widget().selectedItems()]


def main():
    app = QApplication(sys.argv)
    p = PlayerAdminView()
    p.show()
    app.exec_()

if __name__ == '__main__':
    main()
