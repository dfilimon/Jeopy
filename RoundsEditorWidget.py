import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class RoundsEditor(QWidget):

    def __init__(self, parent = None):

        super(RoundsEditor, self).__init__(parent)

    def setupGui(self):

        self.frame = QGridLayout()
        self.setLayout(self.frame)

        label = QLabel("Rounds:")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont(QFont.defaultFamily(label.font()), 10))
        self.frame.addWidget(label, 0, 0)

        
        self.layout = QGridLayout()
        self.frame.addLayout(self.layout, 1, 0)

        # adding Save button
        buttonLayout = QGridLayout() # in case we need another button
        saveButton = QPushButton("Save")
        saveButton.setFixedWidth(100)
        buttonLayout.addWidget(saveButton, 0, 0)
        self.frame.addLayout(buttonLayout, 2, 0)
        saveButton.clicked.connect(self.saveGame)

        self.count = -1 # number of rounds created
        
        self.addRound()
        self.getLineEdit(self.count).setFocus()

        
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

        self.getLineEdit(self.count).textChanged.connect(self.enableButton)

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
                
                w = self.getLabelNumber(self.count)
                self.layout.removeWidget(w)
                w.setParent(None)
                
                w = self.getLineEdit(self.count)
                self.layout.removeWidget(w)
                w.setParent(None)
                
                w = self.getButton(self.count)
                self.layout.removeWidget(w)
                w.setParent(None)

                self.frame.setSizeConstraint(QLayout.SetFixedSize) #perfeeeect:X, i love this line
                
                self.count -= 1
                self.getButton(self.count).setEnabled(False)

    def saveGame(self):
        for i in range(self.count):
            print "Round %d: "%i, self.getLineEdit(i).text()
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
