# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from src.GameHall import game_hall_room_button
from src.Networking.game_room_manager import GameRoomManager

class GameHallRoomGird(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)

        self.btns = []
        self.roomManager = GameRoomManager()

        self.setStyleSheet("background-color: rgba(0, 0, 0, 0)")
        self.scrollFrame = QFrame(self)
        self.scrollFrame.setGeometry(0, 0, 550, 450)

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setGeometry(0, 0, 550, 450)
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

        self.addBtn = QPushButton()
        self.addBtn.setObjectName("btnSpecial")
        self.addBtn.setStyleSheet(
        '''
        QPushButton#btnSpecial {
        border-image: url(:add_bg);
        background-repeat: no-repeat;
        }
        QPushButton#btnSpecial:pressed {
        border-image: url(:add_pressed_bg);
        background-repeat: no-repeat;
        }
        ''')
        self.addBtn.setMinimumSize(120, 120)
        self.addBtn.clicked.connect(self.createRoom)
        self.gLayout.addWidget(self.addBtn, 0, 0)

        self.loadingLbl = QLabel(self.addBtn)
        self.loadingLbl.setGeometry(0, 0, 120, 120)
        self.loadingLbl.setHidden(True)
        self.loadingLbl.setContentsMargins(0, 0, 0, 0)
        self.movie = QMovie("res/loading.gif")
        self.movie.setScaledSize(QSize(120, 120))
        self.movie.setSpeed(70)
        self.loadingLbl.setMovie(self.movie)

        self.connect(GameRoomManager(), SIGNAL('refreshRooms'), self.refreshData)
        self.refreshData()

    def createRoom(self):
        self.showLoading()
        rslt = GameRoomManager().createRoom()
        if not rslt:
            self.hideLoading()

    def refreshData(self):
        for idx, btn in enumerate(self.btns):
            self.gLayout.removeWidget(btn)
            btn.deleteLater()
        self.gLayout.update()

        self.btns = []

        for idx, room in enumerate(self.roomManager.rooms):
            i = idx + 1
            roomBtn = game_hall_room_button.GameHallRoomButton(room, self)
            roomBtn.setMinimumSize(120, 120)
            roomBtn.setUserCount(len(GameRoomManager().rooms[i - 1].users))
            self.btns.append(roomBtn)
            self.gLayout.addWidget(roomBtn, i / 4, i % 4)

        self.hideLoading()

    def showLoading(self):
        self.addBtn.setEnabled(False)
        self.loadingLbl.setHidden(False)
        self.movie.start()

    def hideLoading(self):
        self.addBtn.setEnabled(True)
        self.loadingLbl.setHidden(True)
        self.movie.stop()