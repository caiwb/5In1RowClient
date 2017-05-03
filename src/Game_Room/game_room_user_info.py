# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import game_room_manager
import login_manager

class GameRoomUserInfo(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.setStyleSheet("GameRoomUserInfo{background-color: rgba(0, 0, 0, 0)}")
        self.setGeometry(530, 20, 255, 50)
        self.roomManager = game_room_manager.GameRoomManager()
        self.loginManager = login_manager.LoginManager()
        self.connect(self.roomManager, SIGNAL('refreshRoom'),
                     self.refreshData)
        self.setup()
        self.refreshData()

    def setup(self):
        font = QFont()
        font.setPointSize(12)

        self.myInfoLbl = QLabel(self)
        self.myInfoLbl.setGeometry(0, 0, 120, 50)
        self.myInfoLbl.setAlignment(Qt.AlignLeft)
        self.myInfoLbl.setFont(font)

        self.rivalInfoLbl = QLabel(self)
        self.rivalInfoLbl.setGeometry(130, 0, 120, 50)
        self.rivalInfoLbl.setAlignment(Qt.AlignLeft)
        self.rivalInfoLbl.setFont(font)

    def refreshData(self):
        room = self.roomManager.room
        if not room:
            return
        for user in self.roomManager.room.users:
            if user.uid == self.loginManager.currentUser.uid:
                self.myInfoLbl.setText(u'我方：%s  \n得分：%d' %
                                       (user.account, user.score))
            else:
                self.rivalInfoLbl.setText(u'敌方：%s  \n得分：%d' %
                                          (user.account, user.score))

        if len(self.roomManager.room.users) == 1:
            self.rivalInfoLbl.setText('')
