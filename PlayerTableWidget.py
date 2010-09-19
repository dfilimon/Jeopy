from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Player:
    def __init__(self, name = '', score = 0):
        self.name = name
        self.score = score
    def getName(self):
        return self.name
    def getScore(self):
        return self.score

class PlayerTable(QWidget):
    
    def __init__(self, parent = None):
        super(PlayerTable, self).__init__(parent)
        self.setupGui()

    def addPlayer(self, player):
        table = self.getTable()
        table.insertRow(0)
        table.setItem(0, 0, QTableWidgetItem(player.getName()))
        table.setItem(0, 1, QTableWidgetItem(str(player.getScore())))
        table.sortItems(1, Qt.DescendingOrder)

    def setupGui(self):
        table = QTableWidget()
        table.setColumnCount(2)
        table.setHorizontalHeaderLabels(['Nickname', 'Score'])
        table.setSortingEnabled(True)
        
        table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setResizeMode(QHeaderView.Stretch)
        
        layout = QGridLayout()
        layout.addWidget(table)
        self.setLayout(layout)        

    def getTable(self):
        return self.layout().itemAt(0).widget()

def main():
    import sys
    app = QApplication(sys.argv)
    w = PlayerTable()

    w.addPlayer(Player('dan', 34))
    w.addPlayer(Player('alice', 42))
    w.addPlayer(Player('eve', 2))
    
    w.show()
    app.exec_()

if __name__ == '__main__':
    main()
