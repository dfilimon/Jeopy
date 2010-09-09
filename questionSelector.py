import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class QuestionSelector(QWidget):
    def __init__(self, m, n, categoryLabels, scores, labelFontSize=20, scoreFontSize=12, parent = None):
        super(QuestionSelector, self).__init__(parent)

        layout = QGridLayout()
        
        for i in range(n):
            w = QLabel(categoryLabels[i])
            self.setFontSize(w, labelFontSize)
            layout.addWidget(w, 0, i)
        
        for i in range(m):
            for j in range(n):
                w = QPushButton(str(scores[i][j]))
                self.setFontSize(w, scoreFontSize)
                layout.addWidget(w, i + 1, j)

        for i in range(layout.rowCount()):
            for j in range(layout.columnCount()):
                w = layout.itemAtPosition(i, j).widget()
                w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                
        """for i in range(layout.numCols()):
            #print layout.columnStretch(i)
            layout.setColumnMinSize(i, 
        print [layout.columnStretch(i) for i in range(layout.columnCount())]"""
        
        layout.setHorizontalSpacing(20)
        self.setLayout(layout)

        self.l = [ [lambda x: self.sayHi(x, i, j) for i in range(1, layout.rowCount())] for j in range(layout.columnCount()) ]
        for i in range(1, layout.rowCount()):
            for j in range(layout.columnCount()):
                w = layout.itemAtPosition(i, j).widget()
                self.connect(w, SIGNAL('clicked(bool)'), self.l[i - 1][j])
                self.l[i - 1][j](True)
                #self.connect(w, SIGNAL('clicked(bool)'), self.emitClicked)

        #self.connect(self, SIGNAL('questionSelected(int,int)'), self.sayHi)

    def setFontSize(self, widget, fontSize):
        widget.setFont(QFont(QFont.defaultFamily(widget.font()), fontSize))

    def emitClicked(self):
        print 'emitting', self.sender()
        index = self.layout().indexOf(self.sender())
        n = self.layout().columnCount()

        print index / n, index % n
        
        self.emit(SIGNAL('questionSelected(int,int)'), index / n, index % n)

    def sayHi(self, x, i, j):
        print 'Question', i, j

def main():
    app = QApplication(sys.argv)

    q = QuestionSelector(m=3, n=3, categoryLabels=['cookies', 'milk', 'crayons'], scores=[[10, 10, 10], [20, 20, 20], [30, 30, 30]], labelFontSize = 32, scoreFontSize=24)

    win = QMainWindow()
    win.setCentralWidget(q)
    win.show()
    
    app.exec_()

if __name__ == '__main__':
    main()
