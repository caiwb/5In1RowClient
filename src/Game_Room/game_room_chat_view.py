# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import game_room_manager
import login_manager

class GameRoomChatView(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self)
        self.setStyleSheet("GameRoomChatView{background-color: rgba(0, 0, 0, 100)}")
        self.setGeometry(530, 200, 255, 300)
        # self.setGeometry(530, 20, 255, 50)