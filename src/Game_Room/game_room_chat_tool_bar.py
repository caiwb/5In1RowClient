# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import game_room_manager
import login_manager
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

class GameRoomChatToolBar(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.setGeometry(530, 480, 255, 30)

        self.textEdit = QLineEdit(self)
        self.textEdit.setGeometry(0, 0, 200, 30)
        self.textEdit.setFocusPolicy(Qt.ClickFocus)

        self.sendBtn = QPushButton(self)
        self.sendBtn.setGeometry(205, 0, 50, 30)
        self.sendBtn.setText(u'发送')
        self.sendBtn.clicked.connect(self.sendText)
        self.sendBtn.setFocusPolicy(Qt.ClickFocus)

    def sendText(self):
        logging.debug(self.textEdit.text())
        game_room_manager.GameRoomManager().chat(str(_toUtf8(self.textEdit.text())))
