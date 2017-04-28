# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import game_hall_room_button
import copy

class GameHallRoomGird(QFrame):
    def __init__(self, parent=None, rooms=[]):
        QFrame.__init__(self, parent)

        self.__rooms = rooms
        self.btns = []

        self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.scrollFrame = QFrame(self)
        self.scrollFrame.setGeometry(0, 0, 600, 533)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setGeometry(0, 0, 520, 450)
        self.scrollArea.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                                  QSizePolicy.Expanding))
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollFrame)

        self.gLayout = QGridLayout()
        self.gLayout.setHorizontalSpacing(10)
        self.gLayout.setVerticalSpacing(10)

        self.gLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.scrollFrame.setLayout(self.gLayout)

        addBtn = QPushButton()
        addBtn.setObjectName("btnSpecial")
        addBtn.setStyleSheet(
        '''
        QPushButton#btnSpecial {
        border-image: url(res/add_bg.png);
        background-repeat: no-repeat;
        }
        QPushButton#btnSpecial:pressed {
        border-image: url(res/add_pressed_bg.png);
        background-repeat: no-repeat;
        }
        ''')
        addBtn.setMinimumSize(120, 120)
        self.gLayout.addWidget(addBtn, 0, 0)

        self.refreshData()

    @property
    def rooms(self, value):
        if isinstance(value, list):
            self.__rooms = copy.deepcopy(value)
            self.refreshData()

    def refreshData(self):
        for idx, btn in enumerate(self.btns):
            self.gLayout.removeWidget(btn)
            btn.deleteLater()

        for i in range(1 + len(self.__rooms)):
            if not i:
                continue
            roomBtn = game_hall_room_button.GameHallRoomButton(self)
            roomBtn.setMinimumSize(120, 120)
            roomBtn.setUserCount(self.__rooms[i].users)
            self.btns.append(roomBtn)
            self.gLayout.addWidget(roomBtn, i / 4, i % 4)





