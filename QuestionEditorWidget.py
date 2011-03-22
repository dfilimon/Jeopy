import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class QuestionEditor(QWidget):

    def __init__(self, parent = None):

        super(QuestionEditor, self).__init__(parent)

    def setupGui(self, i):
        
        frame = QGridLayout()
        self.setLayout(frame)



        self.layout = QGridLayout()
        label = QLabel("Question %d:" % i)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont(QFont.defaultFamily(label.font()), 10))

        
        frame.addWidget(label, 0, 0)
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
        valueSpinBox.setValue(100)
        #valueSpinBox.setSuffix(" p")

        self.layout.addWidget(QLabel("Statement:"), 0, 0)
        self.layout.addWidget(QLabel("Answer:"), 1, 0)
        self.layout.addWidget(QLabel("Value:"), 2, 0)
        self.layout.addWidget(statementLine, 0, 1)
        self.layout.addWidget(answerLine, 1, 1)
        self.layout.addWidget(valueSpinBox, 2, 1)

        # adding Save and Cancel buttons
        buttonLayout = QGridLayout()
        saveButton = QPushButton("Save")
        cancelButton = QPushButton("Cancel")
        buttonLayout.addWidget(saveButton, 0, 0)
        buttonLayout.addWidget(cancelButton, 0, 1)
        self.layout.addLayout(buttonLayout, 3, 1)


        self.layout.addLayout

        self.layout.itemAtPosition(0, 0).widget().setAlignment(Qt.AlignRight)
        self.layout.itemAtPosition(1, 0).widget().setAlignment(Qt.AlignRight)
        self.layout.itemAtPosition(2, 0).widget().setAlignment(Qt.AlignRight)
        self.layout.itemAtPosition(2, 1).setAlignment(Qt.AlignCenter)

        statementLine.setAlignment(Qt.AlignCenter)
        answerLine.setAlignment(Qt.AlignCenter)
        valueSpinBox.setAlignment(Qt.AlignCenter)
        
        statementLine.setFocus()
        statementLine.selectAll()

        saveButton.clicked.connect(self.saveQuestion)
        cancelButton.clicked.connect(self.closeWindow)
        
    def saveQuestion(self):
        statement = self.layout.itemAtPosition(0, 1).widget().text()
        answer = self.layout.itemAtPosition(1, 1).widget().text()
        value = self.layout.itemAtPosition(2, 1).widget().text()
        print statement
        print answer
        print value
        self.closeWindow()

    def closeWindow(self):
        self.close()



                
def main():
    app = QApplication(sys.argv)
    gui = QuestionEditor()
    gui.setupGui(3)
    gui.show()
    app.exec_()

if __name__ == '__main__':
    main()
