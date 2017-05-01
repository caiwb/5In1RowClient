# -*- encoding: UTF-8 -*-

from PyQt4.QtCore import *
import json, logging
import network_client
import game_room_manager
from user_model import UserModel

def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton

@singleton
class LoginManager(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.client = network_client.TcpClient()
        self.currentUser = None
        self.isLogin

    def login(self, account):
        reqData = {'sid': 1000,
                   'cid': 1000,
                   'account': account}
        jsonReq = json.dumps(reqData)

        callbackKey = '1000_1000'
        self.client.callbacksDict[callbackKey] = self.loginCallback
        self.client.send(jsonReq)
        logging.debug('login send' + jsonReq)

    def loginCallback(self, response, data):
        allKeys = ['user', 'result', 'code', 'reason']
        if [False for key in allKeys if key not in response.keys()]:
            logging.debug('login resp key error')
            return
        if response['result']:
            userDict = response['user']
            self.currentUser = UserModel(userDict)

        self.emit(SIGNAL("loginCallback(int, int)"),
                  response['result'], response['code'])

    def logout(self):
        pass

    @property
    def isLogin(self):
        return True if self.currentUser else False
