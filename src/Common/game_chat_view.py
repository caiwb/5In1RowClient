# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from src.Networking import game_play_manager
from src.Networking import game_room_manager

class GameChatView(QListView):
    def __init__(self, parent=None):
        QListView.__init__(self, parent)

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
