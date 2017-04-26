#-*- encoding: UTF-8 -*-

from PyQt4.QtCore import *
import json

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

class LoginManager(QObject):
    def __init__(self, client):
        QObject.__init__(self)
        self.client = client
        self.isLogin = False
        self.currentUser = -1

    def login(self, user, callback):
        reqData = {'sid': 0,
                   'cid': 0,
                   'user': user}
        jsonReq = json.dumps(reqData)

        callbackKey = '0_0'
        self.client.callbacksDict[callbackKey] = callback
        self.client.send(jsonReq)

    def logout(self):
        pass
