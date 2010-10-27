from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib.pyplot as plt
import tempfile

class PlotRenderer(QThread):
    finishedPlot = pyqtSignal(str)

    def __init__(self, scores, filePath, drawLegend, dpi, parent):
        super(PlotRenderer, self).__init__(parent)
        self.scores = scores
        self.filePath = filePath    
        self.drawLegend = drawLegend
        self.dpi = dpi
    
    def run(self):
        scores = self.scores
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.hold(True)

        hue = 0
        hueInc = 360 / len(scores)
        
        for player in scores.items():
            color = QColor()
            color.setHsv(hue, 255, 240)
            hue += hueInc - 1
            x = range(1, len(player[1]) + 1)
            ax.plot(x, player[1], color = color.getRgbF(), label = player[0])

        if self.drawLegend:
            ax.legend(loc = 'best')
            
        #linePlotPath = tempfile.mkstemp(suffix = '.png', dir = path)[1]
        plt.savefig(self.filePath, dpi = self.dpi)

        self.finishedPlot.emit(self.filePath)
        self.exec_()

        
