from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Player:
    def __init__(self, name = '', score = 0, ip = '0.0.0.0', status = ''):
        self.name = name
        self.score = score
        self.ip = ip
        self.status = status

        print self.name, self.score, self.status, self.ip
    def getName(self):
        return self.name
    def getScore(self):
        return self.score
    def getIp(self):
        return self.ip
    def getStatus(self):
        return self.status
    

class PlayerAdminTable(QWidget):

    playersMuted = pyqtSignal(list)
    playersUnmuted = pyqtSignal(list)
    
    def __init__(self, buttonText, parent = None):
        super(PlayerAdminTable, self).__init__(parent)
        self.setupGui(buttonText)
        self.layout().itemAtPosition(1, 0).widget().clicked.connect(self.mutePlayers)
        self.layout().itemAtPosition(1, 1).widget().clicked.connect(self.unmutePlayers)

    def addPlayer(self, player):
        table = self.getTable()
        table.insertRow(0)

        table.setItem(0, 0, QTableWidgetItem(player.getName()))
        table.setItem(0, 1, QTableWidgetItem(player.getIp()))
        table.setItem(0, 2, QTableWidgetItem(player.getStatus()))
        table.setItem(0, 3, QTableWidgetItem(str(player.getScore())))

        table.sortItems(3, Qt.DescendingOrder)

    def setupGui(self, buttonText):
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(['Nickname', 'IP', 'Status', 'Score'])
        table.setSortingEnabled(True)
        
        table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        table.verticalHeader().setResizeMode(QHeaderView.Stretch)
        
        layout = QGridLayout()
        layout.addWidget(table, 0, 0, 1, 2)
        layout.addWidget(QPushButton(buttonText.title()), 1, 0)
        layout.addWidget(QPushButton('Un' + buttonText), 1, 1)
        
        self.setLayout(layout)

    def getTable(self):
        return self.layout().itemAt(0).widget()

    def getSelected(self):
        return [str(item.text()) for item in self.getTable().selectedItems()]

    def mutePlayers(self):
        self.playersMuted.emit(self.getSelected())

    def unmutePlayers(self):
        self.playersUnmuted.emit(self.getSelected())

def main():
    import sys
    app = QApplication(sys.argv)
    w = PlayerAdminTable('ban')

    w.addPlayer(Player('dan', 34, status= 'Waiting'))
    w.addPlayer(Player('alice', 42, status='Busy'))
    w.addPlayer(Player('eve', 2, status='Wn'))
    
    w.show()
    app.exec_()

if __name__ == '__main__':
    main()
