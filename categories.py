from PyQt4.QtCore import *
from PyQt4.QtGui import *

class categoryGrid(QWidget):
	def __init__(self, i):
		super(categoryGrid, self).__init__()
		self.layout = QGridLayout()
		self.layout.setHorizontalSpacing(5)
		self.setLayout(self.layout)
	
		self.buttons = []
		
		self.setupGui(i)

	def setupGui(self, i):
		for m in range(i):
			widget = QLineEdit()
			self.buttons.append(widget)
			widget.setMaxLength(30)
			#w.setMaximumWidth(100)
			self.layout.addWidget(widget, 0, m)

	def add(self, i):
		widget = QLineEdit()
		self.layout.addWidget(widget, 0, i)
		self.buttons.append(widget)
		widget.show()

	def rem(self, i):
		self.buttons[-1].hide()
		self.layout.removeWidget(self.buttons[-1])
		self.buttons.remove(self.buttons[-1])
		#del self.buttons[-1:]
