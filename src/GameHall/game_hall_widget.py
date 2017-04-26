# -*- encoding: UTF-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import logging
import game_hall_topbar_frame
import game_hall_main_frame
import game_hall_manager
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
        self.loginManager = login_manager.LoginManager(self.client)
        self.gameHallManager = game_hall_manager.GameHallManager(self.client)

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
        self.connect(self.loginDialog, SIGNAL("close"),
                     self.loginDialogClose)
        self.connect(self.loginDialog, SIGNAL("login(QString,int,QString)"),
                     self.login)
        self.loginDialog.open()

    def loginDialogClose(self):
        if not self.loginManager.isLogin:
            self.loginDialog = login_dialog.LoginDialog(self)
            self.connect(self.loginDialog, SIGNAL("close"),
                         self.loginDialogClose)
            self.connect(self.loginDialog, SIGNAL("login(QString,int,QString)"),
                         self.login)
            self.loginDialog.open()

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
                self.loginManager.login(user, self.loginComplete)
            else:
                raise Exception('connect failed')
        except Exception as e:
            logging.debug(e.message)

            errDailog = QMessageBox(self)
            errDailog.warning(None, u'登录失败',
                              u'服务器连接失败，请检查地址和端口号是否错误',
                              u'确定')
            errDailog.buttonClicked.connect(self.loginDialogClose)

            self.loginDialog.hideLoading()

    def loginComplete(self, response):
        if not isinstance(response, dict):
            suc = False
            reason = u'登录失败，请重新登录'
            return
        elif response.has_key('result') and response.has_key('reason'):
            suc = response['result']
            reason = response['reason']

        self.loginDialog.hideLoading()
        if suc:
            sucDailog = QMessageBox(self)
            sucDailog.information(None, u'登录成功',
                                  u'登录成功，尽情享受游戏的乐趣吧',
                                  u'确定')
            sucDailog.buttonClicked.connect(self.loginDialogClose)
        else:
            logging.debug(reason)
            errDailog = QMessageBox(self)
            errDailog.warning(None, u'登录失败', reason, u'确定')
            errDailog.buttonClicked.connect(self.loginDialogClose)

    def closeWindow(self):
        # if self.client:
        #     self.client.close()
        self.loginDialog.done(1)
        self.close()
