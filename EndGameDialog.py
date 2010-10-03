from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PlayerTableWidget import PlayerTable
from LinePlotThread import LinePlotThread

class EndGameDialog(QDialog):

    def __init__(self, scores, path, parent = None):
        super(EndGameDialog, self).__init__(parent)
        self.setupGui(scores, path)

    def setupGui(self, scores, path):
        layout = QGridLayout()
        self.setLayout(layout)

        table = PlayerTable(['Nickname', 'Score'], '')
        for player in scores.items():
            table.addPlayer((player[0], player[1][-1]))
            
        layout.addWidget(table, 0, 0)
        layout.addWidget(QLabel('Rendering plot...'), 0, 1)

        plotThread = LinePlotThread(scores, path, self)
        plotThread.finishedPlot.connect(self.loadPlot)
        plotThread.start()

    def loadPlot(self, path):
        self.pixmap = QPixmap(path)
        self.layout().itemAt(1).widget().setPixmap(self.pixmap.scaled(800, 600, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        
        
        
    
    
