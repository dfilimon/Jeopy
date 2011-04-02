import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import grid
import categories

class mainWindow(QWidget):
	def __init__(self, title='default', width = 600, height = 400, parent=None):
		super(mainWindow, self).__init__(parent)
		
		#self.setMinimumSize(800, 600)
		self.setMinimumSize(width, height)
		self.setWindowTitle(title)
		
		ButSize = QSize(40, 40)

		self.remColumn = QToolButton()
		self.remColumn.setIcon(QIcon("remc.png"))
		self.remColumn.setIconSize(ButSize)
		
		self.addColumn = QToolButton()
		self.addColumn.setIcon(QIcon("addc.png"))
		self.addColumn.setIconSize(ButSize)	
	
		self.i = 2 
		self.j = 2
		self.categories = categories.categoryGrid(self.i)	
	
		self.DisplayQ = grid.Grid(self.i, self.j)
		#self.DisplayQ.setMinimumSize(600, 600)

		self.remRow = QToolButton()
		self.remRow.setIcon(QIcon("remr.png"))
		self.remRow.setIconSize(ButSize)
		
		self.addRow = QToolButton()
		self.addRow.setIcon(QIcon("addr.png"))
		self.addRow.setIconSize(ButSize)	
		
		layout = QGridLayout()
		
		layout.addWidget(self.remColumn, 2 ,0)
		layout.addWidget(self.addColumn, 2, 1, Qt.AlignLeft)
		layout.addWidget(self.categories, 0, 1)
		layout.addWidget(self.DisplayQ, 1, 1)
		layout.addWidget(self.remRow, 0, 2)
		layout.addWidget(self.addRow, 1, 2, Qt.AlignTop)

		self.setLayout(layout)

		self.connect(self.remColumn, SIGNAL("clicked()"), lambda action="remColumn": self.updateUI(action))
		
		self.connect(self.addColumn, SIGNAL("clicked()"), lambda action = "addColumn": self.updateUI(action))
		
		self.connect(self.addRow, SIGNAL("clicked()"), lambda action = "addRow": self.updateUI(action))
	
		self.connect(self.remRow, SIGNAL("clicked()"), lambda action = "remRow": self.updateUI(action))

	def updateUI(self, action):
		if action == "remColumn":
			if self.i > 0:
				self.i = self.i - 1
				self.categories.rem(self.i)
				self.DisplayQ.remColumn(self.i, self.j)
		
		if action == "addColumn":
			self.i = self.i + 1
			self.categories.add(self.i)
			self.DisplayQ.addColumn(self.i, self.j)

		if action == "remRow":
			if self.j > 0:
				self.j = self.j -1
				self.DisplayQ.remRow(self.i, self.j)

		if action == "addRow":
			self.j = self.j + 1
			self.DisplayQ.addRow(self.i, self.j)

            
def main():
	app = QApplication(sys.argv)
	form =  mainWindow()
	form.show()
	app.exec_()	

if __name__ == '__main__':
	main()
