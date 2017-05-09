#-*- encoding: UTF-8 -*-

import threading
from lib import netstream
import time
import logging
import json
from src.Networking import game_user_manager
from PyQt4.QtCore import *

def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton

@singleton
class TcpClient(netstream.netstream):

    def __init__(self):
        netstream.netstream.__init__(self, 8)
        self.isConnnecting = False
        self.shutdown = False
        self.callbacksDict = {}
        self.hbTimer = time.time()
        self.hbTimeoutCount = 0
        self.loopThread = threading.Thread(target=self.processing)
        self.loopThread.setDaemon(True)
        self.hbThread = threading.Thread(target=self.hbLoop)
        self.hbThread.setDaemon(True)

    def connect(self, address='127.0.0.1', port=7890,
                head=-1, block=False, timeout=0):
        suc = netstream.netstream.connect(self, address, port,
                                          head, block, timeout)
        if suc == 0:
            self.isConnnecting = True
            self.loopThread.start()
            self.hbThread.start()
            return 0
        return -1

    def processing(self):
        while not self.shutdown:
            time.sleep(0.1)
            self.process()
            if self.status() == netstream.NET_STATE_ESTABLISHED:
                while True:
                    data = self.recv()
                    if data:
                        if data == 'hb':
                            logging.debug("--------hb recv--------")
                            self.hbTimeoutCount = 0
                            self.hbTimer = time.time()
                            self.send('hb')
                            continue
                        logging.debug('recv' + data)
                        response = json.loads(data)
                        if 'sid' in response and 'cid' in response:
                            sid = response['sid']
                            cid = response['cid']
                            callbackKey = '%d_%d' % (sid, cid)
                            try:
                                callback = self.callbacksDict[callbackKey]
                                callback(response, data)
                            except:
                                logging.warning('callback err ' + callbackKey)

            elif self.status() == netstream.NET_STATE_STOP:
                game_user_manager.GameUserManager().emit(SIGNAL("showLogin"))

    def hbLoop(self):
        while True:
            t = time.time()
            if t - self.hbTimer > 20:
                logging.debug('--------hb timeout--------')
                self.hbTimeoutCount += 1
                self.hbTimer = t
            if self.hbTimeoutCount > 3:
                logging.debug('--------hb close--------')
                self.close()
                game_user_manager.GameUserManager().emit(SIGNAL("showLogin"))
                break