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
        self.registRoomListCallBack()

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
            logging.debug('create room suc')

    def requestRoomList(self):
        reqData = {'sid': 1,
                   'cid': 1}
        jsonReq = json.dumps(reqData)
        self.client.send(jsonReq)
        logging.debug('request room list send' + jsonReq)

    def registRoomListCallBack(self):
        callbackKey = '1_1'
        self.client.callbacksDict[callbackKey] = self.roomListCallback

    def roomListCallback(self, response, data):
        allKeys = ['result', 'code', 'rooms']
        if [False for key in allKeys if key not in response.keys()]:
            logging.debug('room list key error')
            return
        if response['result']:
            roomsDict = response['rooms']
            for roomDict in roomsDict:
                room = RoomModel(roomDict)
                self.rooms.append(room)
        self.emit(SIGNAL("refreshRoom"))
