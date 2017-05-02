from PyQt4.QtGui import *


class GameRoomUserInfo(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.setStyleSheet("GameRoomUserInfo{background-color: rgba(0, 0, 0, 100)}")
        self.setGeometry(530, 15, 255, 100)
        self.setup()

    def setup(self):
        self.myInfoLbl = QLabel(self)
        self.rivalInfoLbl = QLabel(self)

    def refreshData(self):
        pass