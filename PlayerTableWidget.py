from PyQt4.QtCore import *
from PyQt4.QtGui import *

class PlayerTable(QWidget):

    playersMuted = pyqtSignal(list)
    playersUnmuted = pyqtSignal(list)
    
    def __init__(self, labels, buttonText, parent = None):
        super(PlayerTable, self).__init__(parent)
        self.setupGui(labels, buttonText)

        if buttonText != '':
            self.layout().itemAtPosition(1, 0).widget().clicked.connect(self.mutePlayers)
            self.layout().itemAtPosition(1, 1).widget().clicked.connect(self.unmutePlayers)


    def addPlayer(self, player):
        table = self.getTable()
        table.insertRow(0)

        for i in range(len(player)):
            table.setItem(0, i, QTableWidgetItem(str(player[i])))

        table.sortItems(3, Qt.DescendingOrder)

        self.updateTableWidth()
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def updatePlayer(self, player):
        table = self.getTable()
        name = player[0]
        print 'admintable updating', player
        table.setSortingEnabled(False)
        
        for r in range(table.rowCount()):
            #print table.itemAt(r, 0).text()
            if table.item(r, 0).text() == name:
                for i in range(1, len(player)):
                    table.setItem(r, i, QTableWidgetItem(str(player[i])))
                break

        table.setSortingEnabled(True)
        table.sortItems(len(player) - 1, Qt.DescendingOrder)
        self.updateTableWidth()
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)

                


    def setupGui(self, labels, buttonText):
        layout = QGridLayout()
        self.setLayout(layout)

        table = QTableWidget()
        layout.addWidget(table, 0, 0, 1, 2)

        table.setColumnCount(len(labels))
        table.setHorizontalHeaderLabels(labels)
        
        table.setSortingEnabled(True)
        table.setShowGrid(False)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        #table.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #table.horizontalHeader().setResizeMode(1, QHeaderView.Stretch)
        #table.horizontalHeader().setStretchLastSection(True)
        #table.verticalHeader().setResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setSortIndicatorShown(False)
        self.updateTableWidth()
        #table.setFixedWidth(self.getTableWidth())
        

        if buttonText != '':
            layout.addWidget(QPushButton(buttonText.title()), 1, 0)
            layout.addWidget(QPushButton('Un' + buttonText), 1, 1)


    def getTable(self):
        return self.layout().itemAt(0).widget()

    def getTableWidth(self):
        table = self.getTable()
        width = 0
        
        for c in range(table.columnCount()):
            width += table.columnWidth(c)
            #table.horizontalHeader().resizeSection(c, table.columnWidth(c))
        width += table.verticalHeader().width() + 2
        return width

    def updateTableWidth(self):
        table = self.getTable()
        table.resizeColumnsToContents()
        width = self.getTableWidth()
        
        table.setFixedWidth(width)

    def getSelected(self):
        return [str(item.text()) for item in self.getTable().selectedItems()]


    def mutePlayers(self):
        self.playersMuted.emit(self.getSelected())


    def unmutePlayers(self):
        self.playersUnmuted.emit(self.getSelected())



"""
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
"""
