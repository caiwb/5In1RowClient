# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import game_hall_room_gird

class GameHallMain(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.setStyleSheet(
        '''
        GameHallMain{
        border-image: url(res/background.jpg);
        background-repeat: no-repeat;
        }
        ''')
        self.setGeometry(0, 67, 800, 533)

        self.roomGird = game_hall_room_gird.GameHallRoomGird(self)
        self.roomGird.setGeometry(40, 40, 520, 450)
