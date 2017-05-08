# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from src.GameRoom import game_room_chess_board
from src.GameRoom import game_room_user_info
from src.GameRoom import game_room_btns_frame
from src.Networking import game_play_manager
from src.GameRoom import game_room_result_frame
from src.GameRoom import game_room_chat_view
from src.GameRoom import game_room_chat_tool_bar

class GameRoomMain(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.setStyleSheet(
        '''
        GameRoomMain{
        border-image: url(:background);
        background-repeat: no-repeat;
        }
        ''')
        self.setGeometry(0, 67, 800, 533)

        self.chessBoardFrame = game_room_chess_board.ChessBoard(self)
        self.userInfoFrame = game_room_user_info.GameRoomUserInfo(self)
        self.btnsFrame = game_room_btns_frame.GameRoomBtnsFrame(self)
        self.chatTable = game_room_chat_view.GameRoomChatView(self)
        self.chatToolBar = game_room_chat_tool_bar.GameRoomChatToolBar(self)

        self.connect(game_play_manager.GamePlayManager(),
                     SIGNAL("chessResult(int)"), self.showResult)
        self.connect(game_play_manager.GamePlayManager(),
                     SIGNAL("redo(int)"), self.chessBoardFrame.redo)

    def showResult(self, win):
        self.resultFrame = game_room_result_frame.GameRoomResultFrame(win, self)
        self.resultFrame.show()
        self.chessBoardFrame.connect(self.resultFrame, SIGNAL("clear"),
                                     self.chessBoardFrame.clear)


