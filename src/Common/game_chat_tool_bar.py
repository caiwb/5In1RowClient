# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import logging

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _toUtf8 = QString.toUtf8
except AttributeError:
    def _toUtf8(s):
        return s


class GameChatToolBar(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.textEdit = QLineEdit(self)
        self.textEdit.setFocusPolicy(Qt.ClickFocus)

        self.sendBtn = QPushButton(self)
        self.sendBtn.setText(u'发送')
        self.sendBtn.clicked.connect(self.sendText)
        self.sendBtn.setFocusPolicy(Qt.ClickFocus)

        self.updateLayout()

    def sendText(self):
        self.parent().sendText(str(_toUtf8(self.textEdit.text())))
        self.textEdit.clear()

    def updateLayout(self):
        width = (self.width() - 5) / 5
        self.textEdit.setGeometry(0, 0, width * 4, 30)
        self.sendBtn.setGeometry(width * 4 + 5, 0, width, 30)

