#-*- encoding: UTF-8 -*-

from base_network_client import BaseClient

class GameHallClient(BaseClient):
    def __init__(self):
        BaseClient.__init__(self)

    def requestTableData(self, callback):
        pass
