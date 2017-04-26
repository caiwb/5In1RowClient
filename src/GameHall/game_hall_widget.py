#-*- encoding: UTF-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import game_hall_topbar_frame
import game_hall_main_frame
import login_dialog

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

class GameHallMainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # data source
        self.tableList = []
        # ui
        self.resize(800, 600)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint |
                            Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.topbarFrame = game_hall_topbar_frame.GameHallTopBar(self)
        self.mainFrame = game_hall_main_frame.GameHallMain(self)
        self.loginDialog = login_dialog.LoginDialog(self)
        self.loginDialog.open()
        self.connect(self.loginDialog, SIGNAL("close"),
                     self.loginDialogClose)
        self.connect(self.loginDialog, SIGNAL("login(QString,QString,QString)"),
                     self.login)


    def loginDialogClose(self):
        pass

    def login(self, ip, port, user):
        pass