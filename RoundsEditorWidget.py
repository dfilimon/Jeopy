import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from gameEditor import mainWindow

class RoundsEditor(QWidget):

    buttonClicked = pyqtSignal(int)
    
    def __init__(self, parent = None):

        super(RoundsEditor, self).__init__(parent)

        self.type = "html"
        self.template = "template.html"
        self.size = {}
        self.rounds = []

    def setupGui(self):
        self.frame = QGridLayout()
        self.setLayout(self.frame)

        label = QLabel("Rounds:")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont(QFont.defaultFamily(label.font()), 10))
        self.frame.addWidget(label, 0, 0)

        # adding size buttons
        sizes = QGridLayout()
        self.widthSpin = QDoubleSpinBox()
        self.widthSpin.setRange(0, 3000)
        self.widthSpin.setSingleStep(100)
        self.widthSpin.setDecimals(0)
        self.widthSpin.setFixedWidth(80)
        self.widthSpin.setValue(600)
        
        self.heightSpin = QDoubleSpinBox()
        self.heightSpin.setRange(0, 3000)
        self.heightSpin.setSingleStep(100)
        self.heightSpin.setDecimals(0)
        self.heightSpin.setFixedWidth(80)
        self.heightSpin.setValue(400)

        sizes.addWidget(QLabel("Width:"), 0, 0)
        sizes.addWidget(self.widthSpin, 0, 1)
        sizes.addWidget(QLabel("Height:"), 0, 2)
        sizes.addWidget(self.heightSpin, 0, 3)
        self.frame.addLayout(sizes, 1, 0)

        self.widthSpin.valueChanged.connect(self.values)
        self.heightSpin.valueChanged.connect(self.values)
        
        
        self.layout = QGridLayout()
        self.frame.addLayout(self.layout, 2, 0)

        # adding Save button
        buttonLayout = QGridLayout() # in case we need another button
        saveButton = QPushButton("Save")
        saveButton.setFixedWidth(100)
        buttonLayout.addWidget(saveButton, 0, 0)
        self.frame.addLayout(buttonLayout, 3, 0) # added last in the grid
        saveButton.clicked.connect(self.saveGame)

        self.count = -1 # number of rounds created
        
        self.addRound()
        self.getLineEdit(self.count).setFocus()

    def values(self):
        self.size["width"] = self.widthSpin.value()
        self.size["height"] = self.heightSpin.value()
        print self.size
        
    def addRound(self):
        self.count += 1
        
        lineedit = QLineEdit()
        lineedit.setFixedWidth(200)
        button = QPushButton("Edit")
        button.setEnabled(False)
        button.setFixedWidth(40)
        button.setFixedHeight(22)

        self.layout.addWidget(QLabel("%d." %(self.count+1)), self.count, 0)
        self.layout.addWidget(lineedit, self.count, 1)
        self.layout.addWidget(button, self.count, 2)

        self.rounds.append({"buttonFontSize":14, "labelFontSize":18, "title":""})
    
        button.clicked.connect(self.editRound)
        self.getLineEdit(self.count).textChanged.connect(self.enableButton)
        
    def removeRound(self):
        w = self.getLabelNumber(self.count)
        self.layout.removeWidget(w)
        w.setParent(None)
        
        w = self.getLineEdit(self.count)
        self.layout.removeWidget(w)
        w.setParent(None)
        
        w = self.getButton(self.count)
        self.layout.removeWidget(w)
        w.setParent(None)

        self.frame.setSizeConstraint(QLayout.SetFixedSize) #resizes window
        
        self.count -= 1
        self.rounds = self.rounds[:-1] #removing last entry from list
        self.getButton(self.count).setEnabled(False)
        
    def enableButton(self, string):

        button = self.getButton(self.count) # button -> last made button
        lineedit = self.getLineEdit(self.count) # lineedit -> last made lineedit

        if lineedit.hasFocus() == True:        
            if string == "":
                button.setEnabled(False)
            else:
                button.setEnabled(True)
                self.addRound()
        else:
            if self.getLineEdit(self.count-1).text() == "": # if second to last one is empty, remove last one
                self.removeRound()


    def editRound(self):
        row = (self.layout.indexOf(self.sender())-2) /3
        
        #before editing the round, the round list must be updated
        aux = str(self.getLineEdit(row).text()) # adding round to list

        self.rounds[row]["title"] = aux
        self.size["width"] = int(self.widthSpin.value())
        self.size["height"] = int(self.heightSpin.value())
        
        print "button is on row: ", row
        print self.rounds
        
        round_ =  mainWindow(self.rounds[row]['title'], self.size["width"], self.size["height"])
        round_.show()

    def saveGame(self):
        self.rounds = self.rounds[:-1]
        print self.rounds
        self.close()
        
    def getLabelNumber(self, i):
        return self.layout.itemAtPosition(i, 0).widget()

    def getLineEdit(self, i):
        return self.layout.itemAtPosition(i, 1).widget()
        
    def getButton(self, i):
        return self.layout.itemAtPosition(i, 2).widget()

                
def main():
    app = QApplication(sys.argv)
    gui = RoundsEditor()
    gui.setupGui()
    gui.show()
    app.exec_()

if __name__ == '__main__':
    main()
