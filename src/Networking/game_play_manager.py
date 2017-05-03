#-*- encoding: UTF-8 -*-

from PyQt4.QtCore import *
import json, logging
import game_room_manager
from login_manager import LoginManager
import network_client

def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton

#confirm type
CONFIRM_START   = 0
CONFIRM_REDO    = 1
CONFIRM_GIVE_UP = 2

#confirm side
CONFIRM_REQUEST  = 0
CONFIRM_RESPONSE = 1

#chess
NONE_CHESS  = 0
WHITE_CHESS = 1
BLACK_CHESS = 2

@singleton
class GamePlayManager(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.client = network_client.TcpClient()
        self.isStarting = False
        self.chessType = -1
        self.isYourTurn = False
        self.isConfirming = False
        self.registConfirmCallback()
        self.registChessCallback()
        self.registWinCallback()

    # 操作确认
    def confirm(self, side, type):
        if not LoginManager().isLogin or not game_room_manager.GameRoomManager().room:
            return 0
        if type == CONFIRM_START and self.isStarting:
            return 0
        if (type == CONFIRM_REDO or type == CONFIRM_GIVE_UP) and not self.isStarting:
            return 0
        if self.isConfirming:
            return 0

        self.isConfirming = True
        reqData = {'sid': 1002,
                   'cid': 1000,
                   'uid': LoginManager().currentUser.uid,
                   'rid': game_room_manager.GameRoomManager().room.roomId,
                   'type': type,
                   'chess_type': 3 - self.chessType,
                   'side': side}
        jsonReq = json.dumps(reqData)
        self.client.send(jsonReq)
        logging.debug('confirm send' + jsonReq)

    def registConfirmCallback(self):
        callbackKey = '1002_1000'
        self.client.callbacksDict[callbackKey] = self.confirmCallback

    def confirmCallback(self, response, data):
        allKeys = ['result', 'side', 'type']
        if [False for key in allKeys if key not in response.keys()]:
            logging.warning('confirm callback key error')
            return
        if not response['result']:
            return
        if response['side'] == CONFIRM_REQUEST:
            type = int(response['type'])
            self.emit(SIGNAL("requestWithType(int)"), type)
        elif response['side'] == CONFIRM_RESPONSE:
            type = int(response['type'])
            self.isConfirming = False
            # 开始游戏确认
            if type == CONFIRM_START and response.has_key('chess'):
                self.isStarting = True
                self.emit(SIGNAL("start"))
                self.chessType = response['chess']
                if self.chessType == BLACK_CHESS:
                    self.isYourTurn = True
            elif type == CONFIRM_REDO and response.has_key('step') and\
                    response.has_key('chess_type'):
                stepCount = response['step']
                self.isYourTurn = True if \
                    response['chess_type'] == self.chessType else False
                self.emit(SIGNAL("redo(int)"), stepCount)

    #下棋
    def chess(self, x, y):
        if not LoginManager().isLogin or not game_room_manager.GameRoomManager().room:
            return 0
        if self.chessType == -1 or x > 14 or y > 14 or x < 0 or y < 0:
            return 0

        reqData = {'sid': 1002,
                   'cid': 1001,
                   'uid': LoginManager().currentUser.uid,
                   'rid': game_room_manager.GameRoomManager().room.roomId,
                   'type': self.chessType,
                   'x': x,
                   'y': y}

        jsonReq = json.dumps(reqData)
        self.client.send(jsonReq)
        logging.debug('chess send' + jsonReq)

    def registChessCallback(self):
        callbackKey = '1002_1001'
        self.client.callbacksDict[callbackKey] = self.chessCallback

    def chessCallback(self, response, data):
        allKeys = ['result', 'x', 'y', 'type']
        if [False for key in allKeys if key not in response.keys()]:
            logging.warning('chess callback key error')
            return
        if response['result']:
            self.isYourTurn = not self.isYourTurn
            self.emit(SIGNAL("chess(int,int,int)"), response['x'],
                      response['y'], response['type'])

    # win
    def registWinCallback(self):
        callbackKey = '1002_1002'
        self.client.callbacksDict[callbackKey] = self.winCallback

    def winCallback(self, response, data):
        allKeys = ['type']
        if [False for key in allKeys if key not in response.keys()]:
            logging.warning('chess callback key error')
            return
        type = response['type']
        win = 1 if self.chessType == type else 0
        self.isStarting = False
        self.isYourTurn = False
        self.isConfirming = False
        self.chessType = -1
        self.emit(SIGNAL("chessResult(int)"), win)





