# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from src.GameHall import game_hall_room_gird
from src.GameHall import game_hall_rank_list
from src.Common import game_chat_tool_bar
from src.Common import game_chat_view
from src.Networking import game_user_manager

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
        border-image: url(:background);
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
        self.rankList.setGeometry(600, 55, 190, 180)

        self.chatView = game_chat_view.GameChatView(self)
        self.chatView.setStyleSheet(
            '''
            border-image: url(:btn_bg);
            background-repeat: no-repeat;
            ''')
        self.chatView.setGeometry(600, 250, 190, 220)

        self.chatToolBar = game_chat_tool_bar.GameChatToolBar(self)
        self.chatToolBar.setGeometry(600, 480, 190, 30)
        self.chatToolBar.updateLayout()

        self.chatView.connect(game_user_manager.GameUserManager(),
                                 SIGNAL(
                                     "showHallTextWithRGB(QString,int,int,int)"),
                                 self.chatView.showText)

    def sendText(self, s):
        game_user_manager.GameUserManager().chat(s)