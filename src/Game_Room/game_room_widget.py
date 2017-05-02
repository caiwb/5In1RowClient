# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import game_room_main_frame
import game_topbar_frame
import game_room_manager


class GameRoomWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
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
