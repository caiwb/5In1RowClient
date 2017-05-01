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
        self.roomId = None
        self.registRoomListCallBack()

    # 创建房间
    def createRoom(self):
        if not LoginManager().isLogin:
            return -1
        if self.roomId:
            return -1
        reqData = {'sid': 1001,
                   'cid': 1000,
                   'uid': LoginManager().currentUser.uid}
        jsonReq = json.dumps(reqData)

        callbackKey = '1001_1000'
        self.client.callbacksDict[callbackKey] = self.createRoomCallback
        self.client.send(jsonReq)
        logging.debug('create room send' + jsonReq)

    # 创建房间回调
    def createRoomCallback(self, response, data):
        allKeys = ['rid', 'result', 'code']
        if [False for key in allKeys if key not in response.keys()]:
            logging.warning('create room callback resp key error')
            return
        if response['result']:
            self.roomId = response['rid']
            self.emit(SIGNAL("enterRoom"))
            logging.debug('create room suc')

    # 请求房间列表
    def requestRoomList(self):
        reqData = {'sid': 1001,
                   'cid': 1001}
        jsonReq = json.dumps(reqData)
        self.client.send(jsonReq)
        logging.debug('request room list send' + jsonReq)

    # 注册房间列表广播回调
    def registRoomListCallBack(self):
        callbackKey = '1001_1001'
        self.client.callbacksDict[callbackKey] = self.roomListCallback

    # 房间列表回调
    def roomListCallback(self, response, data):
        allKeys = ['result', 'code', 'rooms']
        if [False for key in allKeys if key not in response.keys()]:
            logging.warning('room list callback key error')
            return
        if response['result']:
            self.rooms = []
            roomsDict = response['rooms']
            for roomDict in roomsDict:
                room = RoomModel(roomDict)
                self.rooms.append(room)
            self.emit(SIGNAL("refreshRoom"))

    # 进入房间
    def enterRoom(self):
        if not LoginManager().isLogin:
            return
        reqData = {'sid': 1001,
                   'cid': 1002,
                   'uid': LoginManager().currentUser.uid}
        jsonReq = json.dumps(reqData)

        callbackKey = '1001_1002'
        self.client.callbacksDict[callbackKey] = self.createRoomCallback
        self.client.send(jsonReq)
        logging.debug('enter room send' + jsonReq)

    # 进入房间回调
    def enterRoomCallback(self, response, data):
        allKeys = ['result', 'code', 'rid']
        if [False for key in allKeys if key not in response.keys()]:
            logging.warning('enter room callback key error')
            return
        if response['result']:
            self.roomId = response['rid']
            self.emit(SIGNAL("enterRoom"))
        pass

    # 退出房间
    def leaveRoom(self):
        pass

    # 退出房间回调
    def leaveRoomCallback(self):
        pass
