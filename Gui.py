from PyQt4.QtCore import *
from PyQt4.QtGui import *

from string import Template
import tempfile
import os

from ButtonGridWidget import ButtonGrid
from QuestionDisplayWidget import QuestionDisplay

from LinePlotThread import LinePlotThread

class Gui(QWidget):

    def __init__(self, parent = None):
        super(Gui, self).__init__(parent)

    def setupGui(self, buttonText, width, height):
        layout = QGridLayout()
        self.setLayout(layout)

        w = QLabel()
        w.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        w.setFont(QFont(QFont.defaultFamily(w.font()), 32))
        layout.addWidget(w, 0, 1)
        layout.addLayout(QStackedLayout(), 1, 0)
        layout.addWidget(self.setupTable(), 1, 1)

        self.width = width
        self.height = height
        w = ButtonGrid(self.getRound(), width = self.width, height = self.height)
        self.getStack().addWidget(w)

        w = QuestionDisplay('html', self.getTemplate(), self.getTempPath(), buttonText, width = width, height = height)
        self.getStack().addWidget(w)

        self.setupSignals()

    def __del__(self):
        self.deleteTempFiles()
        super(Gui, self).__del__()

    def displayQuestion(self, i):
        self.getGrid().layout().itemAt(i).widget().setEnabled(False)
        print 'displaying question...'
        question = self.getQuestion()
        template = self.getTemplateFromQuestion(question)
        answer = question['answer']
        question['answer'] = ''
        #print template
        #print question
        statement = Template(template).substitute(question)
        question['answer'] = answer
        #print statement
        self.getDisplay().updateGui(statement, self.getTempPath())
        self.getStack().setCurrentIndex(1)

    def displayAnswer(self):
        question = self.getQuestion()
        template = self.getTemplateFromQuestion(question)
        answer = Template(template).substitute(question)
        self.getDisplay().updateGui(answer, self.getTempPath())

    def displayGrid(self):
        self.getStack().setCurrentIndex(0)

    def getLabel(self):
        return self.layout().itemAtPosition(0, 1).widget()

    def getStack(self):
        return self.layout().itemAtPosition(1, 0).layout()

    def getGrid(self):
        return self.getStack().itemAt(0).widget()

    def updateGrid(self):
        print 'updating grid'
        oldGrid = self.getStack().takeAt(0).widget()
        del oldGrid
        self.getStack().insertWidget(0, ButtonGrid(self.getRound(), width = self.width, height = self.height))

    def deleteTempFiles(self):
        path = self.getTempPath()
        for name in os.listdir(path):
            os.remove(path + '/' + name)
        os.removedirs(path)

    def displayEndGame(self):
        plotThread = LinePlotThread(self.getScores(), self.getTempPath(), self)
        plotThread.finishedPlot.connect(self.displayPlot)
        self.getLabel().hide()

        print 'rendering plot...'
        w = QLabel()
        w.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        w.setFont(QFont(QFont.defaultFamily(w.font()), 32))
        w.setText('Rendering Plot...')
        self.getStack().insertWidget(0, w)
        self.getStack().setCurrentIndex(0)
        
        plotThread.start()

    def displayPlot(self, path):
        self.pixmap = QPixmap(path)
        self.getStack().itemAt(0).widget().setPixmap(self.pixmap.scaled(self.width, self.height, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))

    def getDisplay(self):
        return self.getStack().itemAt(1).widget()

    def getDisplayButton(self):
        return self.getDisplay().layout().itemAt(1).widget()

    def getTable(self):
        return self.layout().itemAtPosition(1, 1).widget()

    def getRound(self):
        raise NotImplementedError('getRound is virtual and must be overridden')

    def getTemplate(self):
        raise NotImplementedError('getTemplate is virtual and must be overridden')

    def getScores(self):
        raise NotImplementedError('getScores is virtual and must be overridden')        

    def getTemplateFromQuestion(self, question):
        if 'template' not in question or question == None:
            return self.getTemplate()
        templateFile = open(self.getTempPath() + '/' + question['template'])
        return ''.join([ line for line in templateFile.readlines() ])

    def getTempPath(self):
        raise NotImplementedError('getTmpPath is virtual and must be overridden')

    def setupTable(self):
        raise NotImplementedError('setupTable is virtual and must be overridden')

    def setupSignals(self):
        raise NotImplementedError('setupSignals is virtual and must be overridden')
