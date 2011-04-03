from PyQt4.QtCore import *
from PyQt4.QtGui import *

class categoryGrid(QWidget):
	def __init__(self, cols):
		super(categoryGrid, self).__init__()
		
		self.layout = QGridLayout()
		self.layout.setHorizontalSpacing(5)
		self.setLayout(self.layout)
	
		self.buttons = []
		
		self.setupGui(cols)

	def setupGui(self, cols):
		for j in range(cols):
			widget = QLineEdit()
			self.buttons.append(widget)
			widget.setMaxLength(30)
			#w.setMaximumWidth(100)
			self.layout.addWidget(widget, 0, j)
			self.connect(widget, SIGNAL("clicked()"), self.click1)

	def add(self, cols):
		widget = QLineEdit()
		self.layout.addWidget(widget, 0, cols)
		self.buttons.append(widget)
		widget.show()

	def rem(self, cols):
		self.buttons[-1].hide()
		self.layout.removeWidget(self.buttons[-1])
		self.buttons.remove(self.buttons[-1])
		#del self.buttons[-1:]

	def click1(self,):
		o = QuestionEditor(4, "m")

