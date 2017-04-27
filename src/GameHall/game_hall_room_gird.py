# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import game_hall_room_button

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _toUtf8 = QString.toUtf8
except AttributeError:
    def _toUtf8(s):
        return s

class GameHallRoomGird(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.rooms = []

        self.setStyleSheet(
            '''

            background-color: rgba(255,255,255,0)

            '''
        )
        # self.setAttribute(Qt.WA_TranslucentBackground)
        self.scrollFrame = QFrame(self)
        self.scrollFrame.setGeometry(0, 0, 600, 533)
        # self.setStyleSheet(
        #     '''
        #     GameHallRoomGird{
        #     background-color: rgba(255,255,255,0)
        #     }
        #     '''
        # )

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                                  QSizePolicy.Expanding))

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollFrame)


        gLayout = QGridLayout()
        gLayout.setAlignment(Qt.AlignCenter)
        self.scrollFrame.setLayout(gLayout)

        roomBtn = game_hall_room_button.GameHallRoomButton(self)
        roomBtn.setMinimumSize(200, 200)
        gLayout.addWidget(roomBtn, 0, 0)

        roomBtn1 = game_hall_room_button.GameHallRoomButton(self)
        roomBtn1.setMinimumSize(200, 200)
        gLayout.addWidget(roomBtn1, 0, 1)

        roomBtn2 = game_hall_room_button.GameHallRoomButton(self)
        roomBtn2.setMinimumSize(200, 200)
        gLayout.addWidget(roomBtn2, 0, 2)


