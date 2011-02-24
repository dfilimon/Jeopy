"""
Small helper thread to render the final plot using Matplotlib.
Emits finishedPlot signal with a string to the path where the file has been written to.
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import matplotlib.pyplot as plt
import tempfile

class PlotRenderer(QThread):
    finishedPlot = pyqtSignal(str)
    """
    lets the gui know where the plot has been drawn
    """

    def __init__(self, scores, filePath, drawLegend, dpi, parent):
        """
        @param scores: the names, scores and colors of every player
        @type scores: dictionary (keys are player names)
        @param filePath: where to save the drawn plot
        @type filePath: str
        @param drawLegend: whether to draw a legend or not, useful for saving as PNG
        @type drawLegend: bool
        @param dpi: dots per inch for render, the higher it is, the more time it takes
        to draw, default value set in Gui.py is enough to get 800x600, should ideally
        be calculated based on canvas resolution
        @type dpi: int
        """
        super(PlotRenderer, self).__init__(parent)
        self.scores = scores
        self.filePath = filePath
        self.drawLegend = drawLegend
        self.dpi = dpi

    def run(self):
        """
        every thread overwrites run()
        draws line plots for each player with a different color
        also draws a legend if required
        """
        scores = self.scores
        print scores

        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.hold(True)

        for player in scores.items():
            x = range(1, len(player[1][0]) + 1)
            ax.plot(x, player[1][0], color = player[1][1], label = player[0])

        if self.drawLegend:
            ax.legend(loc = 'best')

        #linePlotPath = tempfile.mkstemp(suffix = '.png', dir = path)[1]
        plt.savefig(self.filePath, dpi = self.dpi)

        self.finishedPlot.emit(self.filePath)
        self.exec_()


