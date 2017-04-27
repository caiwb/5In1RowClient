# -*- encoding: UTF-8 -*-

from PyQt4.QtCore import *
import json, logging
from user_model import UserModel

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
        self.currentUser = None
        self.isLogin

    def login(self, account):
        reqData = {'sid': 0,
                   'cid': 0,
                   'account': account}
        jsonReq = json.dumps(reqData)
        logging.debug('login send' + jsonReq)

        callbackKey = '0_0'
        self.client.callbacksDict[callbackKey] = self.loginCallback
        self.client.send(jsonReq)

    def loginCallback(self, response, data):
        allKeys = ['user', 'result', 'code', 'reason']
        if [False for key in allKeys if key not in response.keys()]:
            logging.debug('login resp key error')
            return
        if response['result']:
            userDict = response['user']
            self.currentUser = UserModel(userDict)

        self.emit(SIGNAL("loginCallback(QString)"), data)

    def logout(self):
        pass

    @property
    def isLogin(self):
        return True if self.currentUser else False
