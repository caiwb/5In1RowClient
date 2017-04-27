#-*- encoding: UTF-8 -*-

from network_client import TcpClient
from PyQt4.QtCore import *
import json, logging

class GameRoomManager(QObject):
    def __init__(self, client):
        QObject.__init__(self)
        self.client = client
        self.user = None
        self.rooms = []

    def createRoom(self):
        reqData = {'sid': 1,
                   'cid': 0,
                   'uid': self.user.uid}
        jsonReq = json.dumps(reqData)
        logging.debug('create room send' + jsonReq)

        callbackKey = '1_0'
        self.client.callbacksDict[callbackKey] = self.createRoomCallback
        self.client.send(jsonReq)

    def createRoomCallback(self, response, data): pass
        # allKeys = ['user', 'result', 'code', 'reason']
        # if [False for key in allKeys if key not in response.keys()]:
        #     logging.debug('login resp key error')
        #     return
        # if response['result']:
        #     userDict = response['user']
        #     user = UserModel(userDict)

    def requestRoomList(self):
        reqData = {'sid': 1,
                   'cid': 0}
        jsonReq = json.dumps(reqData)
        logging.debug('request room list send' + jsonReq)

        callbackKey = '1_1'
        self.client.callbacksDict[callbackKey] = self.roomListCallback
        self.client.send(jsonReq)

    def roomListCallback(self, response, data): pass
