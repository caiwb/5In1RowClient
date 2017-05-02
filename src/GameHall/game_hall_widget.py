# -*- encoding: UTF-8 -*-

import logging

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import game_hall_main_frame
import game_topbar_frame
import game_room_manager
import game_room_widget
import login_dialog
import login_manager
import network_client

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

        # network manager
        self.client = network_client.TcpClient()
        self.loginManager = login_manager.LoginManager()
        self.gameRoomManager = game_room_manager.GameRoomManager()
        self.connect(self.loginManager, SIGNAL("loginCallback(int, int)"),
                     self.loginCallback)
        self.connect(self.gameRoomManager, SIGNAL('enterRoom'), self.enterRoom)

        # data source
        self.tableList = []

        # ui
        self.resize(800, 600)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint |
                            Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.topbarFrame = game_topbar_frame.GameTopBar(self, self)
        self.mainFrame = game_hall_main_frame.GameHallMain(self)

        #dialog
        self.loginDialog = login_dialog.LoginDialog(self)
        self.connect(self.loginDialog, SIGNAL("close"),
                     self.loginDialogClose)
        self.connect(self.loginDialog, SIGNAL("login(QString,int,QString)"),
                     self.login)
        self.loginDialog.open()

        self.resultDailog = QMessageBox(self)

    def loginDialogClose(self):
        if self.loginManager.isLogin:
            self.loginDialog.canClose = True
            self.loginDialog.close()

    def login(self, ip, port, user):
        if isinstance(user, QString):
            user = _toUtf8(user).data()
        self.loginDialog.showLoading()
        try:
            if not self.client.isConnnecting:
                suc = self.client.connect(ip, port, -1, False, 7)
            else:
                suc = 0
            if suc == 0:
                self.loginManager.login(user)
            else:
                raise Exception('connect failed')
        except Exception as e:
            logging.debug(e.message)
            self.loginComplete(u'登录失败', u'服务器连接失败，'
                                            u'请检查地址和端口号是否错误')

    def loginCallback(self, suc, code):
        if suc:
            title = u'登录成功'
            reason = u'登录成功，请尽情享受对战的乐趣吧~'
            self.gameRoomManager.requestRoomList()
        else:
            title = u'登录失败'
            reason = u'该账号已登录，请更换账号' if code == 1001 \
                else u'服务器连接失败，请检查地址和端口号是否错误'
        self.loginComplete(title, reason)

    def loginComplete(self, title, reason):
        logging.debug(reason)
        self.loginDialog.hideLoading()
        ret = self.resultDailog.information(None, title, reason,
                                            u'确定')
        if ret == 0:
            self.loginDialogClose()

    def enterRoom(self):
        window = game_room_widget.GameRoomWidget(self)
        window.setWindowTitle(u"五子棋")
        window.show()

    # def closeWindow(self):
    #     self.loginDialog.done(1)
    #     self.close()
