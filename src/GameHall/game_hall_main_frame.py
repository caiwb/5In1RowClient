# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import game_hall_room_gird
import game_hall_rank_list

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
        self.roomGird.setGeometry(40, 40, 550, 450)


        self.rankTitle = QLabel(self)
        self.rankTitle.setText(u'排行榜')
        self.rankTitle.setStyleSheet(_fromUtf8("font: 75 14pt \"微软雅黑\";\n"
                                               "color: rgb(100, 100, 200);"))
        self.rankTitle.setAlignment(Qt.AlignCenter)
        self.rankTitle.setGeometry(600, 20, 190, 20)

        self.rankList = game_hall_rank_list.GameHallRankList(self)
        self.rankList.setGeometry(600, 55, 190, 450)