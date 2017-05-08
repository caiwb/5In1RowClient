# -*- encoding: UTF-8 -*-

from PyQt4.QtCore import *
import json, logging
import network_client
from src.Model.user_model import UserModel

def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton

#sid
USER_SERVICE_ID = 1000

#cid
LOGIN_HANDLER_ID        = 1000
POST_RANK_HANDLER_ID    = 1001
CHAT_IN_HALL_HANDLER_ID = 1002

@singleton
class GameUserManager(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.client = network_client.TcpClient()
        self.currentUser = None
        self.isLogin
        self.userScore = []

        self.registRankCallback()
        self.registChatCallback()

    # 登录请求
    def login(self, account):
        reqData = {'sid': USER_SERVICE_ID,
                   'cid': LOGIN_HANDLER_ID,
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

    # 排行榜
    def rankCallback(self, response, data):
        allKeys = ['users']
        if [False for key in allKeys if key not in response.keys()]:
            logging.debug('rank resp key error')
            return
        self.userScore = response['users']
        self.userScore.sort(key=lambda obj: obj.get('score'), reverse=True)
        self.emit(SIGNAL("refreshRank"))

    def registRankCallback(self):
        callbackKey = '1000_1001'
        self.client.callbacksDict[callbackKey] = self.rankCallback

    # 聊天请求
    def chat(self, text):
        if not self.isLogin:
            return 0
        reqData = {'sid': USER_SERVICE_ID,
                   'cid': CHAT_IN_HALL_HANDLER_ID,
                   'uid': self.currentUser.uid,
                   'text': text}
        jsonReq = json.dumps(reqData)
        self.client.send(jsonReq)
        logging.debug('hall chat text send' + jsonReq)

    def registChatCallback(self):
        callbackKey = '1000_1002'
        self.client.callbacksDict[callbackKey] = self.chatCallback

    def chatCallback(self, response, data):
        allKeys = ['text', 'uid']
        if [False for key in allKeys if key not in response.keys()]:
            logging.warning('chat callback key error')
            return
        text = response['uid'] + ': ' + response['text']
        self.emit(SIGNAL("showHallTextWithRGB(QString,int,int,int)"),
                  text, 0, 0, 0)