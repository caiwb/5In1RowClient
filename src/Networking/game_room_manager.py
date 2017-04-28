#-*- encoding: UTF-8 -*-

from network_client import TcpClient
from PyQt4.QtCore import *
import json, logging
import network_client
from login_manager import LoginManager
from room_model import RoomModel

def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton

@singleton
class GameRoomManager(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.client = network_client.TcpClient()
        self.rooms = []
        self.room = None

    def createRoom(self):
        if not LoginManager().isLogin:
            return
        reqData = {'sid': 1,
                   'cid': 0,
                   'uid': LoginManager().currentUser.uid}
        jsonReq = json.dumps(reqData)

        callbackKey = '1_0'
        self.client.callbacksDict[callbackKey] = self.createRoomCallback
        self.client.send(jsonReq)
        logging.debug('create room send' + jsonReq)

    def createRoomCallback(self, response, data):
        allKeys = ['rid', 'result', 'code', 'rooms']
        if [False for key in allKeys if key not in response.keys()]:
            logging.debug('create room resp key error')
            return
        if response['result']:
            roomsDict = response['rooms']
            for roomDict in roomsDict:
                room = RoomModel(roomDict)
                self.rooms.append(room)
        self.emit(SIGNAL("refreshRoom"))

    def registRoomListCallBack(self):
        reqData = {'sid': 1,
                   'cid': 0}
        jsonReq = json.dumps(reqData)

        callbackKey = '1_1'
        self.client.callbacksDict[callbackKey] = self.roomListCallback
        self.client.send(jsonReq)
        logging.debug('request room list send' + jsonReq)

    def roomListCallback(self, response, data):
        pass
