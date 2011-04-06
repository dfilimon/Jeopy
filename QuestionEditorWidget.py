import sys, os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class QuestionEditor(QDialog):

    def __init__(self, number = -1, round_ = "default", value = 100, parent = None):

        super(QuestionEditor, self).__init__(parent)

        self.defaultValue = value
        self.statement = ''
        self.answer = ''
        self.value = ''
        self.type = 'html'
        self.template = ''

        self.setupGui(number, round_)
        #print self.parent()
 
    def setupGui(self, number, round_):
        
        frame = QGridLayout()
        self.setLayout(frame)

        self.layout = QGridLayout()
        info = QGridLayout()


        roundL = QLabel('Round  "%s"' % round_)
        roundL.setAlignment(Qt.AlignCenter)
        font = QFont.defaultFamily(roundL.font())
        roundL.setFont(QFont(font, 10))
        questionL = QLabel("Question  %d" % number)
        questionL.setAlignment(Qt.AlignCenter)
        questionL.setFont(QFont(font, 10))

        info.addWidget(roundL, 0, 0)
        info.addWidget(questionL, 0, 1)

        
        frame.addLayout(info, 0, 0)
        frame.addLayout(self.layout, 1, 0)

        # inserting all Labels and LineEdit widgets
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

        templateLayout = QGridLayout()
        self.template = 'template.html'
        path = os.path.dirname(sys.argv[0]) + "\\cdl_talk\\template.html"
        path = path.replace('\\', '/')
        self.templateBrowse = QLineEdit(path)
        templateButton = QPushButton("Browse")
        templateButton.setFixedSize(60, 25)

        self.layout.addWidget(QLabel("Statement:"), 0, 0)
        self.layout.addWidget(QLabel("Answer:"), 1, 0)
        self.layout.addWidget(QLabel("Value:"), 2, 0)
        self.layout.addWidget(QLabel("Template:"), 3, 0)
        self.layout.addWidget(statementLine, 0, 1)
        self.layout.addWidget(answerLine, 1, 1)
        self.layout.addWidget(valueSpinBox, 2, 1)

        templateLayout.addWidget(self.templateBrowse, 0, 0)
        templateLayout.addWidget(templateButton, 0, 1)
        self.layout.addLayout(templateLayout, 3, 1)

        # adding Save and Cancel buttons
        buttonLayout = QGridLayout()
        saveButton = QPushButton("Save")
        cancelButton = QPushButton("Cancel")
        buttonLayout.addWidget(saveButton, 0, 0)
        buttonLayout.addWidget(cancelButton, 0, 1)
        self.layout.addLayout(buttonLayout, 4, 1)

        self.layout.itemAtPosition(0, 0).widget().setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.layout.itemAtPosition(1, 0).widget().setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.layout.itemAtPosition(2, 0).widget().setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.layout.itemAtPosition(3, 0).widget().setAlignment(Qt.AlignRight | Qt.AlignCenter)
        self.layout.itemAtPosition(2, 1).setAlignment(Qt.AlignCenter)

        statementLine.setAlignment(Qt.AlignCenter)
        answerLine.setAlignment(Qt.AlignCenter)
        valueSpinBox.setAlignment(Qt.AlignCenter)
        
        statementLine.setFocus()
        statementLine.selectAll()

        templateButton.clicked.connect(self.getTemplate)
        saveButton.clicked.connect(self.saveQuestion)
        cancelButton.clicked.connect(self.close)


    def getTemplate(self):
        self.file = ''
        self.file = str(QFileDialog.getOpenFileName(self,
            'Select a question template', 'template.html', 'Question template (*.html)'))
        print self.file
        if self.file != '':
            self.templateBrowse.setText(self.file)
            self.template = self.file[self.file.rfind('/')+1:]
            
        
        
    def saveQuestion(self):
        self.statement = str(self.layout.itemAtPosition(0, 1).widget().text())
        self.answer = str(self.layout.itemAtPosition(1, 1).widget().text())
        self.value = str(self.layout.itemAtPosition(2, 1).widget().text())
        print self.statement
        print self.answer
        print self.value
        print self.type
        print self.template
        self.close()
        return self.value	

    def closeEvent(self, event):
        print "is this being closed on close / x / save?"
        self.parent().isOpen = False
        #event.accept()



                
def main():
    app = QApplication(sys.argv)
    gui = QuestionEditor()
    gui.show()
    app.exec_()

if __name__ == '__main__':
    main()
