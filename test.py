from __future__ import print_function
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

def main():
	def go():
		print('satan')
	app=QApplication(sys.argv)
	login = QMessageBox(text='please enter name')
	login.setWindowTitle('warning')
	login.setButtonText(1, 'notok')
	if( login.buttons()[0].clicked.connect(go) != None ):
		print('cholera')

	login.show()
	app.exec_()

main()

