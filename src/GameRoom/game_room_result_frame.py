# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class GameRoomResultFrame(QFrame):
    def __init__(self, win, parent=None):
        QFrame.__init__(self, parent)
        self.win = bool(win)

        if win:
            self.setStyleSheet(
            '''
            GameRoomResultFrame{
            border-image: url(:win);
            background-repeat: no-repeat;
            }
            ''')
        else:
            self.setStyleSheet(
            '''
            GameRoomResultFrame{
            border-image: url(:lose);
            background-repeat: no-repeat;
            }
            ''')
        self.setGeometry(220, 100, 350, 321)

        self.okBtn = QPushButton(self)
        self.okBtn.setGeometry(280, 280, 60, 30)
        self.okBtn.setText(u'确定')
        self.okBtn.clicked.connect(self.closeFrame)

    def closeFrame(self):
        self.emit(SIGNAL("clear"))
        self.close()