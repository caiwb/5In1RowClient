#-*- encoding: UTF-8 -*-

from network_client import TcpClient
from PyQt4.QtCore import *

class GameHallManager(QObject):
    def __init__(self, client):
        QObject.__init__(self)
        self.client = client

    def requestTableData(self, callback):
        pass
