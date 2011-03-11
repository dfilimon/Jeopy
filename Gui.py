"""
Defines the base Gui class from which the two versions, ServerGui and PlayerGui
are derived. PlayerGui inherits Gui with few changes, whereas ServerGui uses a
different PlayerTable.
Signals are different and PlayerGui's ButtonGrid doesn't select a question.

    
display* functions modify the visible widget of the QStackedLayoutswitching between the
ButtonGrid and QuestionDisplay:
displayQuestion, displayAnswer
displayGrid : note that, in case of an update (for going to the next round), a different
function is called to replace the buttons, but in the end displayGrid switches th QStackedLayout's current widget
    
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from string import Template
import tempfile
import os

from copy import deepcopy

from ButtonGridWidget import ButtonGrid
from QuestionDisplayWidget import QuestionDisplay

from PlotRenderer import PlotRenderer


class Gui(QWidget):
    gameStarted = pyqtSignal()

    def __init__(self, parent = None):
        super(Gui, self).__init__(parent)
        self.width = None
        self.height = None
        self.pixmap = None # used for score plot at the end of the game
        
    def startGame(self):
        raise NotImplementedError('startGame is virtual and must be overridden')

    def setupGui(self, buttonText, width, height):
        """
        The basic layout is the same - a grid layout with a
        QuestionDisplay / ButtonGrid in a QStackedLayout
        on the left and a PlayerTable on the right.
        The label on top displays informative messages and is hidden when not
        used.
          - buttonText is the text shown in the QuestionDisplay's button
        """
        layout = QGridLayout()
        self.setLayout(layout)

        w = QLabel()
        w.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        w.setFont(QFont(QFont.defaultFamily(w.font()), 28))
        layout.addWidget(w, 0, 1)
        layout.addLayout(QStackedLayout(), 1, 0)
        layout.addWidget(self.setupTable(), 1, 1)

        # width and height of the QuestionDisplay are specified via the 'size' structure in the 'rules.json' file
        self.width = width
        self.height = height
        
        w = ButtonGrid(self.getRound(), width = self.width, height = self.height)
        self.getStack().addWidget(w) # the ButtonGrid will always have index 0

        w = QuestionDisplay('html', self.getTemplate(), self.getTempPath(), buttonText, width = width, height = height)
        self.getStack().addWidget(w) # the QuestionDisplay will always have index 1

        self.setupSignals()

    def setupTable(self):
        raise NotImplementedError('setupTable is virtual and must be overridden')

    def setupSignals(self):
        raise NotImplementedError('setupSignals is virtual and must be overridden')
        
    def deleteTempFiles(self):
        path = self.getTempPath()
        for name in os.listdir(path):
            os.remove(path + '/' + name)
        os.removedirs(path)
 
    def log(self, message):
        """
        messages from different components are prefixed with their source, in this case the gui thread; redirect to create log
        @param message: the message to log
        @type message: str
        """
        print 'Gui: ' + message

    def displayQuestion(self, i):
        """
        displays the current question's statement
        """
        self.getGrid().layout().itemAt(i).widget().setEnabled(False)
        self.log('displaying question ' + str(i))
        
        question = self.getQuestion()
        template = self.getTemplateFromQuestion(question)

        # the template contains an answer placeholder as well, which needs to be erased
        answer = question['answer']
        question['answer'] = ''

        statement = Template(template).substitute(question)

        question['answer'] = answer

        self.getDisplay().updateGui(statement, self.getTempPath())
        self.getStack().setCurrentIndex(1)

    def displayAnswer(self):
        question = self.getQuestion()
        template = self.getTemplateFromQuestion(question)
        answer = Template(template).substitute(question)
        self.getDisplay().updateGui(answer, self.getTempPath())

    def displayGrid(self):
        self.log('displaying grid')
        self.getStack().setCurrentIndex(0)

    def updateGrid(self):
        self.log('updating grid')
        oldGrid = self.getStack().takeAt(0).widget() # the old grid is removed from the QStackedLayout
        del oldGrid
        self.getStack().insertWidget(0, ButtonGrid(self.getRound(), width = self.width, height = self.height))

    def displayEndGame(self):
        """
        Displays the plot drawn by the PlotRenderer. The pixmap getPixmap() returns
        is always scaled down to the appropriate width and height.
        """
        self.getLabel().hide()
        w = QLabel()
        w.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        w.setFont(QFont(QFont.defaultFamily(w.font()), 32))
        w.setText('Rendering plot...')
        self.getStack().addWidget(w)
        self.getStack().setCurrentIndex(2)

        """
        TODO: Color calculation
        hue = 0
        hueInc = 360 / self.getPlayers()
        """
        self.renderPlot()

    def renderPlot(self):
        # generate a random plot path!
        plotPath = tempfile.mkstemp(suffix = '.png', dir = self.getTempPath())[1]

        # 100   <=>   600/800 = 0.75 resolution
        # dpi   <=>   height/width
        dpi = float(self.height) / self.width * 100 / 0.75
        print "current dpi calculated at", dpi ###### -- debug -- ######
        self.plotThread = PlotRenderer(self.getScores(), plotPath, False, dpi, self)
        self.plotThread.finishedPlot.connect(self.displayPlot)
        self.plotThread.start()
        self.log('Renering plot')

    def displayPlot(self, path):
        self.getTable().showColors(self.getColors())
        self.pixmap = QPixmap(path)
        self.getPlot().setPixmap(self.pixmap.scaled(self.width, self.height,
                                                    Qt.KeepAspectRatioByExpanding,
                                                    Qt.SmoothTransformation))
        self.resize(self.minimumSize())
        self.adjustSize()
        self.plotThread.exit()
        print path ################ -- debug -- ################

    def setLabelText(self, message):
        self.getLabel().setText(message)

    """
    Getter functions for the different UI elements
    ----------------------------------------------
    Accessing them manualy would have been awkward and error-prone because of the layout indices.
    """
    def getLabel(self):
        return self.layout().itemAtPosition(0, 1).widget()

    def getStack(self):
        return self.layout().itemAtPosition(1, 0).layout()

    def getTable(self):
        return self.layout().itemAtPosition(1, 1).widget()

    def getGrid(self):
        return self.getStack().itemAt(0).widget()

    def getDisplay(self):
        return self.getStack().itemAt(1).widget()

    def getDisplayButton(self):
        return self.getDisplay().layout().itemAt(1).widget()

    def getGridButton(self, i):
        return self.getGrid().layout().itemAt(i).widget()

    def getPlot(self):
        return self.getStack().itemAt(2).widget()

    def getColors(self):
        """
        Each player is associated a color by dividing the hue range by the number of
        players. When there are lots of players, there is going to be a 'rainbow'
        effect and some colors might be very similar and quite hard to distinguish.
        Perhaps try changing saturation and value as well...?
        """
        return dict([ (player[0], player[1][1])
                      for player in
                      self.getScores().items() ])
    
    """
    These functions get game related data
    -------------------------------------
    This is typically obtained differently for the client and server guis.
    This is why these functions are virtual and their specific implementation is in the derived classes.
    """
    def getRound(self):
        raise NotImplementedError('getRound is virtual and must be overridden')

    def getQuestion(self):
        raise NotImplementedError('getQuestion is virtual and must be overridden')

    def getTempPath(self):
        raise NotImplementedError('getTmpPath is virtual and must be overridden')
    
    def getTemplate(self):
        raise NotImplementedError('getTemplate is virtual and must be overridden')

    def getScores(self):
        raise NotImplementedError('getScores is virtual and must be overridden')

    
    def getTemplateFromQuestion(self, question):
        """
        Helper function, for the case where a question defines a custom html template which needs to be read.
        Is in practice always called, because finding custom templates is not the job of the display{Question,Answer} methods.
        """
        if 'template' not in question or question == None: 
            return self.getTemplate()
        templateFile = open(self.getTempPath() + '/' + question['template'])
        return ''.join([ line for line in templateFile.readlines() ])

