#-*- encoding: UTF-8 -*-

from PyQt4.QtCore import *
import json, logging
from src.Networking import network_client
from src.Networking.login_manager import LoginManager
from src.Networking.game_play_manager import GamePlayManager
from src.Model.room_model import RoomModel

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
        self.registEnterRoomCallback()
        self.registleaveRoomCallback()
        self.registChatCallback()

    # 创建房间
    def createRoom(self):
        if not LoginManager().isLogin:
            return 0
        if self.room:
            return 0
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
        allKeys = ['room', 'result', 'code']
        if [False for key in allKeys if key not in response.keys()]:
            logging.warning('create room callback resp key error')
            return
        if response['result']:
            roomdict = response['room']
            GamePlayManager().isYourTurn = False
            GamePlayManager().isStarting = False
            GamePlayManager().chessType = -1
            self.room = RoomModel(roomdict)
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
            self.emit(SIGNAL("refreshRooms"))

    # 进入房间
    def enterRoom(self, rid):
        if not LoginManager().isLogin:
            return
        if not rid:
            return
        if self.room:
            return
        reqData = {'sid': 1001,
                   'cid': 1002,
                   'rid': rid,
                   'uid': LoginManager().currentUser.uid}
        jsonReq = json.dumps(reqData)

        self.client.send(jsonReq)
        logging.debug('enter room send' + jsonReq)

    # 注册进入房间回调
    def registEnterRoomCallback(self):
        callbackKey = '1001_1002'
        self.client.callbacksDict[callbackKey] = self.enterRoomCallback

    # 进入房间回调
    def enterRoomCallback(self, response, data):
        allKeys = ['result', 'code', 'room']
        if [False for key in allKeys if key not in response.keys()]:
            logging.warning('enter room callback key error')
            return
        if response['result']:
            roomdict = response['room']
            GamePlayManager().isYourTurn = False
            GamePlayManager().isStarting = False
            GamePlayManager().chessType = -1
            logging.debug('enter room suc')
            if not self.room:
                self.emit(SIGNAL('enterRoom'))
                self.room = RoomModel(roomdict)
            else:
                self.room = RoomModel(roomdict)
                self.emit(SIGNAL('refreshRoom'))

    # 退出房间
    def leaveRoom(self):
        if not LoginManager().isLogin:
            return
        if not self.room:
            return
        reqData = {'sid': 1001,
                   'cid': 1003,
                   'rid': self.room.roomId,
                   'uid': LoginManager().currentUser.uid}
        jsonReq = json.dumps(reqData)

        self.client.send(jsonReq)
        logging.debug('leave room send' + jsonReq)

    # 注册退出房间回调
    def registleaveRoomCallback(self):
        callbackKey = '1001_1003'
        self.client.callbacksDict[callbackKey] = self.leaveRoomCallback

    # 退出房间回调
    def leaveRoomCallback(self, response, data):
        allKeys = ['result', 'code']
        if [False for key in allKeys if key not in response.keys()]:
            logging.warning('leave room callback key error')
            return
        if response['result']:
            logging.debug('leave room suc')
            if response['uid'] == LoginManager().currentUser.uid:
                self.room = None
                GamePlayManager().isYourTurn = False
                GamePlayManager().isStarting = False
                GamePlayManager().chessType = -1
            else:
                self.room = RoomModel(response['room'])
            self.emit(SIGNAL('refreshRoom'))

    # 聊天请求
    def chat(self, text):
        if not LoginManager().isLogin:
            return 0
        if not self.room:
            return 0
        reqData = {'sid': 1001,
                   'cid': 1004,
                   'uid': LoginManager().currentUser.uid,
                   'rid': self.room.roomId,
                   'text': text}
        jsonReq = json.dumps(reqData)
        self.client.send(jsonReq)
        logging.debug('chat text send' + jsonReq)

    def registChatCallback(self):
        callbackKey = '1001_1004'
        self.client.callbacksDict[callbackKey] = self.chatCallback

    def chatCallback(self, response, data):
        allKeys = ['text', 'uid']
        if [False for key in allKeys if key not in response.keys()]:
            logging.warning('chat callback key error')
            return
        text = response['uid'] + ': ' + response['text']
        self.emit(SIGNAL("showTextWithRGB(QString,int,int,int)"),
                  text, 0, 0, 0)