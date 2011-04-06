import sys, os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class QuestionEditor(QWidget):

    def __init__(self, number, category, pred, parent = None):

        super(QuestionEditor, self).__init__(parent)

        self.defaultValue = 100
        self.statement = ''
        self.answer = ''
        self.value = ''
        self.type = 'html'
        self.template = ''

        self.setupGui(number, category)
        self.pred = pred
        #print self.parent()
 
    def setupGui(self, number, category):
        
        frame = QVBoxLayout()

        info = QHBoxLayout()
        centerLayout = QGridLayout()
        templateLayout = QHBoxLayout()
        buttonLayout = QHBoxLayout()


        roundL = QLabel('Category  "%s"' % category)
        roundL.setAlignment(Qt.AlignCenter)
        font = QFont.defaultFamily(roundL.font())
        roundL.setFont(QFont(font, 10))
        questionL = QLabel("Question  %d" % number)
        questionL.setAlignment(Qt.AlignCenter)
        questionL.setFont(QFont(font, 10))

        

        # editing all Labels and LineEdit widgets
        statementLine = QLineEdit("Dennis Ritchie")
        statementLine.setFixedWidth(250)
        answerLine = QLineEdit("Who developed C?")

        valueSpinBox = QDoubleSpinBox()
        valueSpinBox.setRange(0, 100000)
        valueSpinBox.setSingleStep(100)
        valueSpinBox.setDecimals(0)
        valueSpinBox.setFixedWidth(80)

        valueSpinBox.setValue(self.defaultValue)
        #valueSpinBox.setSuffix(" p")

        self.template = 'template.html'
        path = os.path.dirname(sys.argv[0]) + "\\cdl_talk\\template.html"
        path = path.replace('\\', '/')
        self.templateBrowse = QLineEdit(path)
        templateButton = QPushButton("Browse")
        templateButton.setFixedSize(60, 25)


        # adding Save and Cancel buttons
        saveButton = QPushButton("Save")
        cancelButton = QPushButton("Cancel")


        # signal setup
        templateButton.clicked.connect(self.getTemplate)
        saveButton.clicked.connect(self.saveQuestion)
        cancelButton.clicked.connect(self.close)


        # layout setup
        info.addWidget(roundL)
        info.addWidget(questionL)

        centerLayout.addWidget(QLabel("Statement:"), 0, 0)
        centerLayout.addWidget(QLabel("Answer:"), 1, 0)
        centerLayout.addWidget(QLabel("Value:"), 2, 0)
        centerLayout.addWidget(QLabel("Template:"), 3, 0)
        centerLayout.addWidget(statementLine, 0, 1)
        centerLayout.addWidget(answerLine, 1, 1)
        centerLayout.addWidget(valueSpinBox, 2, 1)

        templateLayout.addWidget(self.templateBrowse)
        templateLayout.addWidget(templateButton)
        centerLayout.addLayout(buttonLayout, 4, 1)
        centerLayout.addLayout(templateLayout, 3, 1)

        buttonLayout.addWidget(saveButton)
        buttonLayout.addWidget(cancelButton)


        # formating
        centerLayout.itemAtPosition(0, 0).widget().setAlignment(Qt.AlignRight | Qt.AlignCenter)
        centerLayout.itemAtPosition(1, 0).widget().setAlignment(Qt.AlignRight | Qt.AlignCenter)
        centerLayout.itemAtPosition(2, 0).widget().setAlignment(Qt.AlignRight | Qt.AlignCenter)
        centerLayout.itemAtPosition(3, 0).widget().setAlignment(Qt.AlignRight | Qt.AlignCenter)
        centerLayout.itemAtPosition(2, 1).setAlignment(Qt.AlignCenter)

        statementLine.setAlignment(Qt.AlignCenter)
        answerLine.setAlignment(Qt.AlignCenter)
        valueSpinBox.setAlignment(Qt.AlignCenter)
        
        statementLine.setFocus()
        statementLine.selectAll()


        frame.addLayout(info)
        frame.addLayout(centerLayout)

        self.setLayout(frame)


    def getTemplate(self):
        self.file = ''
        self.file = str(QFileDialog.getOpenFileName(self,
            'Select a question template', 'template.html', 'Question template (*.html)'))
        print self.file
        if self.file != '':
            self.templateBrowse.setText(self.file)
            self.template = self.file[self.file.rfind('/')+1:]
            
    
    def getCenterLayout(self):
        return self.layout().itemAt(1).layout()
    
    def saveQuestion(self):
        self.statement = str(self.getCenterLayout().itemAtPosition(0, 1).widget().text())
        self.answer = str(self.getCenterLayout().itemAtPosition(1, 1).widget().text())
        self.value = str(self.getCenterLayout().itemAtPosition(2, 1).widget().text())
        print self.statement
        print self.answer
        print self.value
        print self.type
        print self.template
        self.close()
        return self.value	

    def closeEvent(self, event):
        print "is this being closed on close / x / save?"
        self.pred.isOpen = False

                
def main():
    app = QApplication(sys.argv)
    gui = QuestionEditor()
    gui.show()
    app.exec_()

if __name__ == '__main__':
    main()
