# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import copy

class GameHallRoomButton(QPushButton):
    def __init__(self, parent=None):
        QPushButton.__init__(self, parent)
        self.setObjectName("btnSpecial")
        self.setStyleSheet(
        '''
        GameHallRoomButton#btnSpecial {
        border-image: url(res/btn_bg.png);
        background-repeat: no-repeat;
        }
        GameHallRoomButton#btnSpecial:pressed {
        border-image: url(res/btn_pressed_bg.png);
        background-repeat: no-repeat;
        }
        ''')
        rect = self.rect()

        self.userLbl1 = QLabel(self)
        self.userLbl1.setStyleSheet(
        '''
        border-image: url(res/no_user.png);
        background-repeat: no-repeat;
        ''')
        self.userLbl1.setGeometry(0, 40, 30, 30)

        self.tableLbl = QLabel(self)
        self.tableLbl.setStyleSheet(
        '''
        border-image: url(res/desk.png);
        background-repeat: no-repeat;
        ''')
        self.tableLbl.setGeometry(30, 40, 60, 60)

        self.userLbl2 = QLabel(self)
        self.userLbl2.setStyleSheet(
        '''
        border-image: url(res/no_user.png);
        background-repeat: no-repeat;
        ''')
        self.userLbl2.setGeometry(90, 40, 30, 30)

    def setUserCount(self, count):
        if not count:
            self.userLbl1.setStyleSheet(
            '''
            border-image: url(res/no_user.png);
            background-repeat: no-repeat;
            ''')
            self.userLbl2.setStyleSheet(
            '''
            border-image: url(res/no_user.png);
            background-repeat: no-repeat;
            ''')
        elif count == 1:
            self.userLbl1.setStyleSheet(
            '''
            border-image: url(res/user.png);
            background-repeat: no-repeat;
            ''')
            self.userLbl2.setStyleSheet(
            '''
            border-image: url(res/no_user.png);
            background-repeat: no-repeat;
            ''')
        elif count == 2:
            self.userLbl1.setStyleSheet(
            '''
            border-image: url(res/user.png);
            background-repeat: no-repeat;
            ''')
            self.userLbl2.setStyleSheet(
            '''
            border-image: url(res/user.png);
            background-repeat: no-repeat;
            ''')
