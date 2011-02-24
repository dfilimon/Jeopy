"""
PlayerTable class contains the table displayed at various times throughout Jeopy.
One of these tables is displayed in the PlayerAdminDialog and the others in the Gui (both Player and Admin) and finally it supports colors when drawing the plot at the end.

QTableWidgets are not very cooperative. They need to be specifically forced to a
certain size and the table needs to know that its holding ints, otherwise when
enabling sorting it will do a lexicographic sort, which makes no sense for numbers.
"""

"""
When adding and updating players from a PlayerTable with add() or update(),
the table expects a tuple, that resembles the one used in the GameServer's player
dictionary. Instead of the first element of the tuple being _uri_, it is _name_.

AdminGui:
(name, ip, status, score)
 [0]  [1]   [2]    [3]

PlayerGui:
(name, score)
  [0]   [1]

Invariant:
If our tuple is called player, the sorting is always done after
player[len(player) - 1] which is always the score and contains an int!
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class PlayerTable(QWidget):

    playersMuted = pyqtSignal(list)
    playersUnmuted = pyqtSignal(list)

    """
    There are two basic types of table - the ones displayed in the AdminGui which also contain buttons for muting and unmuting and the ones used in all other cases which don't have any buttons.
    """
    def __init__(self, labels, buttonText, parent = None):
        super(PlayerTable, self).__init__(parent)
        self.setupGui(labels, buttonText)

        if buttonText != '':
            self.layout().itemAtPosition(1, 0).widget().clicked.connect(self.mutePlayers)
            # this is legacy! banning is no longer permitted during login
            # actually working to fix this
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
        #table.setEditTriggers(QAbstractItemView.NoEditTriggers)


    def setupGui(self, labels, buttonText):
        layout = QGridLayout()
        self.setLayout(layout)

        table = QTableWidget()
        # starting at line 0 and column 0, taking up 1 line and 2 columns
        # this way we make sure that buttons (if there are any are properly aligned)
        layout.addWidget(table, 0, 0, 1, 2)

        table.setColumnCount(len(labels))
        table.setHorizontalHeaderLabels(labels)

        table.setSortingEnabled(True)
        table.setShowGrid(False)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        table.horizontalHeader().setSortIndicatorShown(True)
        self.updateTableWidth()

        if buttonText != '':
            if buttonText != 'ban':
                layout.addWidget(QPushButton(buttonText.title()), 1, 0)
                layout.addWidget(QPushButton('Un' + buttonText), 1, 1)
            else:
                layout.addWidget(QPushButton(buttonText.title()), 1, 0, 1, 2)


    def getTable(self):
        return self.layout().itemAt(0).widget()

    def getTableWidth(self):
        """
        set the appropriate table width! needs to work properly!
        currently works but doesn't display sort indicator... maybe I'll come up with
        something better when I stop hating it.
        """
        table = self.getTable()
        width = 0
        table.resizeColumnsToContents()

        for c in range(table.columnCount()):
            if table.horizontalHeader().isSectionHidden(c):
                continue
            width += max(table.columnWidth(c),
                         table.horizontalHeader().sectionSize(c))
            print table.columnWidth(c), table.horizontalHeader().sectionSize(c)

        return width

    def updateTableWidth(self):
        self.getTable().setFixedWidth(self.getTableWidth())

    def getSelected(self):
        return [str(item.text()) for item in self.getTable().selectedItems()]

    def mutePlayers(self):
        self.playersMuted.emit(self.getSelected())

    def unmutePlayers(self):
        self.playersUnmuted.emit(self.getSelected())

    def hideButtons(self):
        self.layout().itemAt(1).widget().hide()
        self.layout().itemAt(2).widget().hide()

    def showColors(self, colors):
        """
        add a column for colors computed according to the colors array.
        @param colors: each tuple contains red green blue alpha information
        @type colors: dictionary of names to tuples
        """
        table = self.getTable()
        table.setColumnCount(table.columnCount() + 1)
        c = table.columnCount() - 1
        table.setHorizontalHeaderItem(c, QTableWidgetItem('Color'))

        if c == 4:
            table.horizontalHeader().hideSection(1)
            table.horizontalHeader().hideSection(2)

        color = QColor()
        for row in range(table.rowCount()):
            (r, g, b, a) = colors[str(table.item(row, 0).text())]
            color.setRgbF(r, g, b, a)
            item = QTableWidgetItem()
            item.setBackground(QBrush(QColor(color)))
            table.setItem(row, c, item)

        self.updateTableWidth()
