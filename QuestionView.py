from PyQt4.QtGui import *
from PyQt4.QtCore import *
from  PyQt4.QtWebKit import *

class QuestionView(QWidget):
    def __init__(self, type, resource, path='', width=800, height=600, parent=None):
        super(QuestionView, self).__init__(parent)

        layout = QVBoxLayout()
        print type, resource
        
        if type == 'image':
            w = QLabel()
            #p = QPixmap('00020_blueblocks_1280x800.jpg')
            #p = p.scaled(QSize(800, 480))
            w.setPixmap(resource.scaled(QSize(width, height)))
        else:
            print path
            w = QWebView()
            w.setHtml(resource, QUrl('file://' + path + '/'))
        w.setFixedSize(width, height)
        
        print w.size().width(), w.size().height()
        
        layout.addWidget(w)

        layout.addWidget(QPushButton())
        layout.itemAt(1).widget().setText('Buzz')

        self.setLayout(layout)

import sys
def main():
    app = QApplication(sys.argv)
    f = open('template.html')
    text = ''
    for line in f:
        text += line
    q = QuestionView('image', QPixmap('test.002.png'), '')
    path = QDir().absolutePath()
    #q = QuestionView('html', text, path, 640, 480)
    win = QMainWindow()
    win.setCentralWidget(q)
    win.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
    print q.size().width(), q.size().height()

    win.show()

    app.exec_()

if __name__ == '__main__':
    main()
    
