# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import game_room_manager

class GameRoomUserInfo(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.setStyleSheet("GameRoomUserInfo{background-color: rgba(0, 0, 0, 100)}")
        self.setGeometry(530, 15, 255, 100)
        self.connect(game_room_manager.GameRoomManager(), SIGNAL('refreshRoom'),
                     self.refreshData)
        self.setup()

    def setup(self):
        self.myInfoLbl = QLabel(self)
        self.rivalInfoLbl = QLabel(self)

    def refreshData(self):
        print 'refresh'