# -*- encoding: UTF-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

import logging, json
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
        self.connect(self.loginManager, SIGNAL("loginCallback(QString)"),
                     self.loginCallback)

        # data source
        self.tableList = []

        # ui
        self.resize(800, 600)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint |
                            Qt.WindowMinMaxButtonsHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.topbarFrame = game_hall_topbar_frame.GameHallTopBar(self)
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
        if not self.loginManager.isLogin:
            self.loginDialog = login_dialog.LoginDialog(self)
            self.connect(self.loginDialog, SIGNAL("close"),
                         self.loginDialogClose)
            self.connect(self.loginDialog, SIGNAL("login(QString,int,QString)"),
                         self.login)
            self.loginDialog.open()
        else:
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

    def loginCallback(self, data):
        if isinstance(data, QString):
            data = _toUtf8(data).data()
        try:
            response = json.loads(data)
        except:
            logging.debug('data is not a json string')
            self.loginComplete(u'登录失败', u'服务器连接失败，'
                                            u'请检查地址和端口号是否错误')
            return
        suc = response['result']
        reason = response['reason']
        code = response['code']

        logging.debug(reason)
        if suc:
            title = u'登录成功'
            reason = u'登录成功，请尽情享受对战的乐趣吧~'
        else:
            title = u'登录失败'
            reason = u'该账号已登录，请更换账号' if code == 1001 \
                else u'服务器连接失败，请检查地址和端口号是否错误'
        self.loginComplete(title, reason)

    def loginComplete(self, title, reason):
        logging.debug(reason)
        self.loginDialog.hideLoading()
        ret = self.resultDailog.information(None, title, reason, QMessageBox.Ok)
        if ret == QMessageBox.Ok:
            self.loginDialogClose()

    def closeWindow(self):
        # if self.client:
        #     self.client.close()
        self.loginDialog.done(1)
        self.close()


