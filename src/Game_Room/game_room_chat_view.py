# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import game_play_manager
import game_room_manager
import login_manager

class GameRoomChatView(QListView):
    def __init__(self, parent=None):
        QListView.__init__(self, parent)
        # self.setStyleSheet("GameRoomChatView{background-color: rgba(0, 0, 0, 100)}")
        self.setGeometry(530, 200, 255, 260)

        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setWordWrap(True)
        self.setUniformItemSizes(True)
        self.setGridSize(QSize(self.rect().width(), 30))
        self.setFont(QFont("Microsoft YaHei", 10))
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAcceptDrops(True)

        self.connect(game_room_manager.GameRoomManager(),
                     SIGNAL("showTextWithRGB(QString,int,int,int)"),
                     self.showText)
        self.connect(game_play_manager.GamePlayManager(),
                     SIGNAL("showTextWithRGB(QString,int,int,int)"),
                     self.showText)
        self.connect(game_room_manager.GameRoomManager(),
                     SIGNAL("clearChat"), self.clear)
        self.connect(game_play_manager.GamePlayManager(),
                     SIGNAL("clearChat"), self.clear)

    def showText(self, text, r=0, g=0, b=0):
        color = QBrush(QColor(r, g, b))
        item = QStandardItem(text)
        item.setTextAlignment(Qt.AlignLeft)
        item.setFont(QFont(50))
        item.setForeground(color)
        self.model.appendRow(item)
        self.scrollTo(self.model.indexFromItem(item),
                      QAbstractItemView.PositionAtCenter)

    def clear(self):
        self.model.clear()
