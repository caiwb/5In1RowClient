# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
import game_room_chess_board
import game_room_user_info

class GameRoomMain(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.setStyleSheet(
        '''
        GameRoomMain{
        border-image: url(res/background.jpg);
        background-repeat: no-repeat;
        }
        ''')
        self.setGeometry(0, 67, 800, 533)

        self.chessBoardFrame = game_room_chess_board.ChessBoard(self)
        self.userInfoFrame = game_room_user_info.GameRoomUserInfo(self)