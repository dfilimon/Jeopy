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
            if buttonText != 'ban':
                self.layout().itemAtPosition(1, 1).widget().clicked.connect(self.unmutePlayers)


    def addPlayer(self, player):
        table = self.getTable()
        table.insertRow(0)

        for i in range(len(player)):
            table.setItem(0, i, QTableWidgetItem(str(player[i])))

        table.sortItems(len(player) - 1, Qt.DescendingOrder)

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
            if buttonText != 'ban':
                layout.addWidget(QPushButton(buttonText.title()), 1, 0)
                layout.addWidget(QPushButton('Un' + buttonText), 1, 1)
            else:
                layout.addWidget(QPushButton(buttonText.title()), 1, 0, 1, 2)


    def getTable(self):
        return self.layout().itemAt(0).widget()

    def getTableWidth(self):
        table = self.getTable()
        width = 0
        
        for c in range(table.columnCount()):
            width += min(table.columnWidth(c),
                         table.horizontalHeader().sectionSize(c))
            
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

    def hideButtons(self):
        self.layout().itemAt(1).widget().hide()
        self.layout().itemAt(2).widget().hide()

    def setColors(self, colors):
        c = table.columnCount() + 1
        table = self.getTable()
        table.setColumnCount(c)
        c -= 1
        table.setHorizontalHeaderItem(c, QTableWidgetItem('Color'))

        for r in range(table.rowCount()):
            (r, g, b) = colors[table.item(r, 0).text()]
            color = QColor()
            color.setRedF = r
            color.setGreenF = g
            color.setBlueF = b
            item = QTableWidgetItem()
            item.setBackground(QBrush(color))
            table.setItem(r, c, item)
