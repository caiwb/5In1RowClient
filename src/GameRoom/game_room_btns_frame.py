# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from src.Networking import game_room_manager
from src.Networking import game_play_manager

#confirm type
CONFIRM_START   = 0
CONFIRM_REDO    = 1
CONFIRM_GIVE_UP = 2

#confirm side
CONFIRM_REQUEST  = 0
CONFIRM_RESPONSE = 1


class GameRoomBtnsFrame(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.gameRoomManager = game_room_manager.GameRoomManager()
        self.gamePlayManager = game_play_manager.GamePlayManager()
        self.setStyleSheet("GameRoomBtnsFrame{background-color: rgba(0, 0, 0, 0)}")
        self.setGeometry(530, 80, 255, 100)
        self.setupBtns()

    def setupBtns(self):
        self.startBtn = QPushButton(self)
        self.startBtn.setObjectName("btnSpecial")
        self.startBtn.setStyleSheet(
        '''
        QPushButton#btnSpecial {
        border-image: url(:chess_btn);
        background-repeat: no-repeat;
        }
        QPushButton#btnSpecial:pressed {
        border-image: url(:chess_btn_press);
        background-repeat: no-repeat;
        }
        ''')
        self.startBtn.setGeometry(10, 10, 100, 40)
        self.startBtn.setText(u'开始')
        self.startBtn.clicked.connect(self.startGame)

        self.redoBtn = QPushButton(self)
        self.redoBtn.setObjectName("btnSpecial")
        self.redoBtn.setStyleSheet(
        '''
        QPushButton#btnSpecial {
        border-image: url(:chess_btn);
        background-repeat: no-repeat;
        }
        QPushButton#btnSpecial:pressed {
        border-image: url(:chess_btn_press);
        background-repeat: no-repeat;
        }
        ''')
        self.redoBtn.setGeometry(120, 10, 100, 40)
        self.redoBtn.setText(u'悔棋')
        self.redoBtn.clicked.connect(self.redo)

        self.giveupBtn = QPushButton(self)
        self.giveupBtn.setObjectName("btnSpecial")
        self.giveupBtn.setStyleSheet(
        '''
        QPushButton#btnSpecial {
        border-image: url(:chess_btn);
        background-repeat: no-repeat;
        }
        QPushButton#btnSpecial:pressed {
        border-image: url(:chess_btn_press);
        background-repeat: no-repeat;
        }
        ''')
        self.giveupBtn.setGeometry(10, 60, 100, 40)
        self.giveupBtn.setText(u'放弃')
        self.giveupBtn.clicked.connect(self.giveupGame)

    def startGame(self):
        if len(self.gameRoomManager.room.users) > 1:
            self.gamePlayManager.confirm(CONFIRM_REQUEST, CONFIRM_START)

    def redo(self):
        if len(self.gameRoomManager.room.users) > 1:
            self.gamePlayManager.confirm(CONFIRM_REQUEST, CONFIRM_REDO)

    def giveupGame(self):
        if len(self.gameRoomManager.room.users) > 1:
            self.gamePlayManager.confirm(CONFIRM_REQUEST, CONFIRM_GIVE_UP)