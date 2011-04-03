from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Grid(QWidget):
	def __init__(self, i, j):
		QWidget.__init__(self)
		
		self.buttons = []
		self.layout = QGridLayout()	
		self.setLayout(self.layout)

		self.setupGui(i, j)
	def setupGui(self, i, j):	
		#layout.setHorizontalSpacing(5)
		self.layout.setSpacing(10)
		for n in range(j): #linie
			for m in range(i): #coloana
				widget = QPushButton()
				self.buttons.append(widget)
				widget.setText(str(n*i+m))
				self.layout.addWidget(widget, n, m)
				widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

	def addRow(self, i, j):
		for n in range(i):
			widget = QPushButton()
			self.buttons.append(widget)
			self.layout.addWidget(widget, j-1, n)
			widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			widget.show() 

	def remRow(self, i, j):
		for n in range(i):
			self.buttons[-1].hide()
			self.layout.removeWidget(self.buttons[-1])
			self.buttons.remove(self.buttons[-1])

	
	def addColumn(self, i, j):
		print "column is %d \n line is %d" % (i, j)
		for m in range(j):
			print 'adding column.. m is: ', m
			widget = QPushButton()
			self.layout.addWidget(widget, m, i-1)
			self.buttons.insert(i-1+m*(i-1)+m, widget)
			widget.setText(str(i-1+m*(i-1)+m))
			widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
			widget.show()

	def remColumn(self, i, j):
		print "i is:", i, "\nj is:", j
		for m in reversed(range(j)):
			print 'rem column.. m is: ', m
			self.buttons[i+(m*(i+1))].hide()
			self.layout.removeWidget(self.buttons[i+(m*(i+1))]) #sau aici
			self.buttons.remove(self.buttons[i+(m*(i+1))])








