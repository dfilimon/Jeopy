"""
The ButtonGrid widget is reponsible for displaying the grid of buttons that correspond to questions in the game as well as the labels for each category.

It supports custom canvas sizes, and reads the size of the fonts to be used from the L{ButtonGrid.round} dictionary that contains the subset of the configuration file required for the current round.
"""
from __future__ import print_function
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class ButtonGrid(QWidget):

	buttonClicked = pyqtSignal(int)


	def __init__(self, round,
				 width = 800, height = 600, parent = None):
		"""
		@param round: Dictionary corresponding to the current round. Should contain the round's title (although it's not currently used) and the array of categories, with each category containing an array of questions.
		@type round: dict
		"""
		super(ButtonGrid, self).__init__(parent)

		self.round = round
		self.width = width
		self.height = height

		self.setupGui(self.round)


	def setupGui(self, round):
		"""
		If there is no font size information available in the dictionary, default to size 12 everywhere.
		"""
		if 'buttonFontSize' not in round:
			buttonFontSize = 12
		else:
			buttonFontSize = round['buttonFontSize']

		if 'labelFontSize' not in round:
			labelFontSize = 12
		else:
			labelFontSize = round['labelFontSize']

		layout = QGridLayout()
		self.setLayout(layout)

		layout.setHorizontalSpacing(5)
		self.setFixedSize(self.width, self.height)


		n = len(round['categories'])

		for i in range(n):
			w = QLabel(round['categories'][i]['title'])
			self.setFontSize(w, labelFontSize)
			w.setAlignment(Qt.AlignCenter)
			w.setWordWrap(True)
			layout.addWidget(w, 0, i)

			m = len(round['categories'][i]['questions'])
			for j in range(m):
				w = QPushButton(str(round['categories'][i]['questions'][j]['value']))
				self.setFontSize(w, buttonFontSize)
				layout.addWidget(w, j + 1, i)
				w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
				w.clicked.connect(self.emitButtonClicked)


	def setFontSize(self, widget, fontSize):
		"""
		Sets the font size for the specified widget.
		@param widget: widget whose font size is to be set
		@type widget: QWidget
		@param fontSize: new font size
		@type fontSize: int
		"""
		widget.setFont(QFont(QFont.defaultFamily(widget.font()), fontSize))

	def emitButtonClicked(self):
		"""
		@return: Not exactly returns, but rather emits the index of the selected question
		"""
		print('emitting', self.sender())
		index = self.layout().indexOf(self.sender())

		self.buttonClicked.emit(index)
