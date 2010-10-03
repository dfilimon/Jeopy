import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ButtonGrid(QWidget):

    buttonClicked = pyqtSignal(int)

    
    def __init__(self, round,
                 width = 800, height = 600, parent = None):
        
        super(ButtonGrid, self).__init__(parent)

        self.round = round
        self.width = width
        self.height = height
        
        self.setupGui(self.round)


    def setupGui(self, round):

        if 'buttonFontSize' not in round:
            buttonFontSize = 12
        else:
            buttonFontSize = round['buttonFontSize']

        if 'labelFontSize' not in round:
            labelFontSize = 12
        else:
            labelFontSize = round['labelFontSize']
        
        layout = QGridLayout()
        self.setLayout(layout)
        
        layout.setHorizontalSpacing(5)        
        self.setFixedSize(self.width, self.height)

        
        n = len(round['categories'])
        
        for i in range(n):
            w = QLabel(round['categories'][i]['title'])
            self.setFontSize(w, labelFontSize)
            w.setAlignment(Qt.AlignCenter)
            w.setWordWrap(True)
            layout.addWidget(w, 0, i)

            m = len(round['categories'][i]['questions'])
            for j in range(m):
                w = QPushButton(str(round['categories'][i]['questions'][j]['value']))
                self.setFontSize(w, buttonFontSize)
                layout.addWidget(w, j + 1, i)
                w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                w.clicked.connect(self.emitButtonClicked)

        #self.buttonClicked.connect(self.sayHi)

    
    def setFontSize(self, widget, fontSize):
        widget.setFont(QFont(QFont.defaultFamily(widget.font()), fontSize))


    def emitButtonClicked(self):
        round = self.round
        print 'emitting', self.sender()
        index = self.layout().indexOf(self.sender())

        self.buttonClicked.emit(index)
            
        #n = self.layout().columnCount()

        #print index, index // n, index % n
        #self.buttonClicked.emit(index // n - 1, index % n)


    def sayHi(self, i, j):
        print 'Question selected: ', i, j

"""
def main():
    app = QApplication(sys.argv)

    q = QuestionGrid(m=3, n=3, categoryLabels=['cookies', 'milk', 'crayons'], scores=[[10, 10, 10], [20, 20, 20], [30, 30, 30]], labelFontSize = 32, scoreFontSize=24)

    win = QMainWindow()
    win.setCentralWidget(q)
    win.show()
    
    app.exec_()

if __name__ == '__main__':
    main()
"""
