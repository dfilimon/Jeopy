#!/usr/bin/env python


from PyQt4 import QtCore, QtGui

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from PlayerTableWidget import PlayerTable
from ButtonGridWidget import ButtonGrid
from QuestionDisplayWidget import QuestionDisplay

class Pixmap(QtGui.QGraphicsObject):
    def __init__(self, pix):
        super(Pixmap, self).__init__()

        self.p = QtGui.QPixmap(pix)

    def paint(self, painter, option, widget):
        painter.drawPixmap(QtCore.QPointF(), self.p)

    def boundingRect(self):
        return QtCore.QRectF(QtCore.QPointF(0, 0), QtCore.QSizeF(self.p.size()))


if __name__ == '__main__':

    import sys

    app = QtGui.QApplication(sys.argv)
    rules = {u'type': u'html', u'rounds': [{u'categories': [{u'questions': [{u'answer': u'What is the meaning of life?', u'value': 300, u'statement': u'42'}, {u'answer': u"What is Steve Jobs' favorite kind of apple?", u'value': 100, u'statement': u'Macintosh'}, {u'answer': u'What is paper made out of?', u'value': 300, u'statement': u'Dead trees'}], u'title': u'Apple Types'}, {u'questions': [{u'answer': u'What is your biggest weakness?', u'value': 32767, u'statement': u'I like cookies'}], u'title': u'Cookies'}], u'title': u'Simple Jeopardy'}, {u'categories': [{u'questions': [{u'answer': u'What makes chicken soup so tasty?', u'value': 1000, u'statement': u'Noodles'}, {u'answer': u'What should you never add to a chicken soup?', u'value': 100, u'statement': u'Nutella'}], u'title': u'Chicken Soup'}], u'title': u' Squared Jeopardy'}], u'template': u'template.html'}



    grid = ButtonGrid(rules['rounds'][0])
    gridProxy = QGraphicsProxyWidget()
    gridProxy.setWidget(grid)

    table = PlayerTable(['alpha', 'beta', 'gamma', 'delta'], 'mute')
    tableProxy = QGraphicsProxyWidget()
    tableProxy.setWidget(table)

    line = QLabel('Random text here')
    lineProxy = QGraphicsProxyWidget()
    lineProxy.setWidget(line)

    text = ''.join([ x for x in open('template.html').readlines() ] )
    display = QuestionDisplay('html', text , '/Users/dan/proj/2/python/jeopardy/new-jeopardy/')
    displayProxy = QGraphicsProxyWidget()
    displayProxy.setWidget(display)


    scene = QtGui.QGraphicsScene(0, 0, 1000, 700)
    scene.setBackgroundBrush(scene.palette().window())
    scene.addItem(lineProxy)
    scene.addItem(gridProxy)
    scene.addItem(displayProxy)
    scene.addItem(tableProxy)

    machine = QtCore.QStateMachine()
    state1 = QtCore.QState(machine)

    state1.assignProperty(line, 'text', 'Random shit')
    state1.assignProperty(line, 'geometry', QRect(500, 0, 200, 30))
    state1.assignProperty(display, 'visible', False)
    state1.assignProperty(table, 'visible', False)
    
    state2 = QtCore.QState(machine)
    
    #state3 = QtCore.QState(machine)
    machine.setInitialState(state1)

    machine.start()

    view = QtGui.QGraphicsView(scene)
    view.show()
    view.setFixedSize(1000, 700)

    sys.exit(app.exec_())

"""

    # State 1.
    state1.assignProperty(button, 'text', "Switch to state 2")
    #state1.assignProperty(widget, 'geometry', QtCore.QRectF(0, 0, 400, 150))
    #state1.assignProperty(box, 'geometry', QtCore.QRect(-200, 150, 200, 150))
    
    state1.assignProperty(boxProxy, 'opacity', 0.0)


    # State 2.
    state2.assignProperty(button, 'text', "Switch to state 3")
    state2.assignProperty(widget, 'geometry', QtCore.QRectF(200, 150, 200, 150))
    state2.assignProperty(box, 'geometry', QtCore.QRect(9, 150, 190, 150))

    state2.assignProperty(boxProxy, 'opacity', 1.0)

    # State 3.
    state3.assignProperty(button, 'text', "Switch to state 1")

    state3.assignProperty(widget, 'geometry', QtCore.QRectF(138, 5, 400 - 138, 200))
    state3.assignProperty(box, 'geometry', QtCore.QRect(5, 205, 400, 90))


    t1 = state1.addTransition(button.clicked, state2)
    animation1SubGroup = QtCore.QSequentialAnimationGroup()
    animation1SubGroup.addPause(250)
    animation1SubGroup.addAnimation(QtCore.QPropertyAnimation(box, 'geometry', state1))
    t1.addAnimation(animation1SubGroup)
    t1.addAnimation(QtCore.QPropertyAnimation(widget, 'geometry', state1))
 

    t2 = state2.addTransition(button.clicked, state3)
    t2.addAnimation(QtCore.QPropertyAnimation(box, 'geometry', state2))
    t2.addAnimation(QtCore.QPropertyAnimation(widget, 'geometry', state2))
  
    t3 = state3.addTransition(button.clicked, state1)
    t3.addAnimation(QtCore.QPropertyAnimation(box, 'geometry', state3))
    t3.addAnimation(QtCore.QPropertyAnimation(widget, 'geometry', state3))

"""

