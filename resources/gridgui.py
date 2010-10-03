import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class GridExample(QWidget):
    def __init__(self, m, n, parent=None):
        super(GridExample, self).__init__(parent)
        self.m = m
        self.n = n

        layout = QGridLayout()
        #self.table = [ [QPushButton(str(j * 100)) for i in range(n)] for j in range(m) ]
        for i in range(m):
            for j in range(n):
                layout.addWidget(QPushButton(str(j * 100)), i + 1, j)
        self.categoryLabels = ['Apples', 'Oranges', 'Lemons', 'Pears', 'Peaches']
        for i in range(5):
            layout.addWidget(QLabel(self.categoryLabels[i]), 0, i)
            w = layout.itemAtPosition(0, i).widget()
            w.setFont(QFont(QFont.defaultFamily(w.font()), 20))
        for i in range(layout.rowCount()):
            for j in range(layout.columnCount()):
                layout.itemAtPosition(i, j).widget().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        for i in range(m):
            layout.itemAtPosition(i + 1, i).widget().setDisabled(True)# = False
        #layout.updateGeometry()
        self.setLayout(layout)

def printUsage():
    print 'Usage: ./gridgui.py <num_lines> <num_cols>'
    sys.exit()
    
def main():
    if len(sys.argv) != 3:
        printUsage()
    else:
        try:
            m = int(sys.argv[1])
            n = int(sys.argv[2])
        except:
            printUsage()

    app = QApplication(sys.argv)
    grid = GridExample(m, n)
    grid.show()
    app.exec_()

if __name__ == '__main__':
    main()
