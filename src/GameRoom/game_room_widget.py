# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from src.GameRoom import game_room_main_frame
from src.Common import game_topbar_frame
from src.Networking import game_room_manager
from src.Networking import game_play_manager
import game_room_result_frame

#confirm type
CONFIRM_START   = 0
CONFIRM_REDO    = 1
CONFIRM_GIVE_UP = 2

#confirm side
CONFIRM_REQUEST  = 0
CONFIRM_RESPONSE = 1


class GameRoomWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.connect(game_play_manager.GamePlayManager(),
                     SIGNAL("requestWithType(int)"), self.showConfirmBox)
        # ui
        self.resize(800, 600)
        self.topbarFrame = game_topbar_frame.GameTopBar(self, self.parent())
        self.mainFrame = game_room_main_frame.GameRoomMain(self)

        # others
        self.canClose = False

    def closeEvent(self, event):
        if not self.canClose:

            ret = QMessageBox(self).information(None, u'确认退出',
                                                u'退出本局游戏将结束，'
                                                u'确认退出房间吗？',
                                                u'确定', u'取消')
            if ret == 0:
                self.canClose = True
                self.close()
                game_room_manager.GameRoomManager().leaveRoom()
            else:
                event.ignore()

    def showConfirmBox(self, type):
        if type == CONFIRM_START:
            title = u'对方请求开始游戏'
        elif type == CONFIRM_REDO:
            title = u'对方请求悔棋'
        elif type == CONFIRM_GIVE_UP:
            title = u'对方放弃'
        ret = QMessageBox(self).information(None, u'确认',title,
                                            u'确定', u'取消')
        if ret == 0:
            game_play_manager.GamePlayManager().confirm(CONFIRM_RESPONSE,
                                                             type)

