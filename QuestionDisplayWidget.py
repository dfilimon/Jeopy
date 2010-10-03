from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

class QuestionDisplay(QWidget):

    buttonClicked = pyqtSignal()

    
    def __init__(self, type_, resource,
                 path = '',
                 buttonText = 'Buzz',
                 width = 800, height = 600, parent = None):
        
        super(QuestionDisplay, self).__init__(parent)

        self.type = type_
        self.buttonText = buttonText
        self.width = width
        self.height = height
        
        self.setupGui(resource, path)
        

    def setupGui(self, resource, path):

        layout = QVBoxLayout()
        self.setLayout(layout)
        
        if self.type == 'image':
            w = QLabel()
        else:
            w = QWebView()
        layout.addWidget(w)
        
        self.updateGui(resource, path)
        
        layout.addWidget(QPushButton(self.buttonText))
        #w.setFixedSize(self.width, self.height)


        self.layout().itemAt(1).widget().clicked.connect(self.buttonClicked.emit)

        self.setFixedSize(self.width, self.height)

        
    def updateGui(self, resource, path):
        
        w = self.layout().itemAt(0).widget()
        
        if self.type == 'image':
            w.setPixmap(resource.scaled(QSize(self.width, self.height)))
        else:
            #print 'HTML load path:', path
            #print resource
            w.setHtml(resource, QUrl('file://' + path + '/'))



"""
import sys
def main():
    app = QApplication(sys.argv)
    f = open('template.html')
    text = ''
    for line in f:
        text += line
    #q = QuestionDisplay('image', QPixmap('test.002.png'))
    path = QDir().absolutePath()
    q = QuestionDisplay('html', text, path, 'Answer', 800, 600)
    win = QMainWindow()
    win.setCentralWidget(q)
    win.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
    print q.size().width(), q.size().height()

    win.show()

    app.exec_()

if __name__ == '__main__':
    main()
"""    
