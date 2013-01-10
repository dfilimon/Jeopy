import sys, os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class QuestionEditor(QWidget):

    def __init__(self, number, category, pred, parent = None):

        super(QuestionEditor, self).__init__(parent)

        self.template = ''

        self.setupGui(number, category)
        self.pred = pred
        self.d = {}
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

        valueSpinBox.setValue(100)
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
        file_ = ''
        file_ = str(QFileDialog.getOpenFileName(self,
            'Select a question template', 'template.html', 'Question template (*.html)'))
        print file_
        if file_ != '':
            self.templateBrowse.setText(file_)
            self.template = file_[file_.rfind('/')+1:]

    def getCenterLayout(self):
        return self.layout().itemAt(1).layout()

    def saveQuestion(self):
        self.d["statement"] = str(self.getCenterLayout().itemAtPosition(0, 1).widget().text());
        self.d["answer"] = str(self.getCenterLayout().itemAtPosition(1, 1).widget().text())
        self.d["value"] = int(self.getCenterLayout().itemAtPosition(2, 1).widget().text())
        self.d["template"] = self.template
        self.pred.d[self.c]["questions"][self.q] = self.d
        # where self.c is the category number [in the "categories" list]
        # and self.q is the question number [in the "questions" list] self.q


        print self.d["statement"]
        print self.d["answer"]
        print self.d["value"]
        print self.d["template"]
        self.close()
        #return self.value

    def closeEvent(self, event):
        print "QuestionEdutir is being closed on 'x, save or cancel'"
        self.pred.isOpen = False


def main():
    app = QApplication(sys.argv)
    gui = QuestionEditor()
    gui.show()
    app.exec_()

if __name__ == '__main__':
    main()
