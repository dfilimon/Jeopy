"""
The Question Display Widget. Obviously.
Can customize size [width, height], and button text.
The widget can also display a pixmap when passed a pixmap and 'image' as a type.
This was intended for a different type game file functionality. It is no longer
supported or used.
"""

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

class QuestionDisplay(QWidget):
	buttonClicked = pyqtSignal()

	def __init__(self, type_, resource,
				 path = '',
				 buttonText = 'Buzz',
				 width = 800, height = 600, parent = None):

		super(QuestionDisplay, self).__init__(parent)

		self.type = type_
		self.buttonText = buttonText
		self.width = width
		self.height = height

		self.setupGui(resource, path)

	def setupGui(self, resource, path):
		layout = QVBoxLayout()
		self.setLayout(layout)

		if self.type == 'image':
			w = QLabel()
		else: # 'html' theoretically; can also set type to 'peanuts' [ps: don't]
			w = QWebView()
		layout.addWidget(w)

		self.updateGui(resource, path)

		layout.addWidget(QPushButton(self.buttonText))
		self.layout().itemAt(1).widget().clicked.connect(self.buttonClicked.emit)
		self.setFixedSize(self.width, self.height)

	"""
	It is essential to pass a full path to setHtml because otherwise images
	and really, any kind of separate file, won't work.
	"""
	def updateGui(self, resource, path):
		w = self.layout().itemAt(0).widget()

		if self.type == 'image':
			w.setPixmap(resource.scaled(QSize(self.width, self.height)))
		else:
			w.setHtml(resource, QUrl('file://' + path + '/'))

