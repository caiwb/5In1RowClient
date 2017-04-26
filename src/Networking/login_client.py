#-*- encoding: UTF-8 -*-

from base_network_client import BaseClient

class LoginClient(BaseClient):
    def __init__(self):
        BaseClient.__init__(self)
        self.isLogin = False
        self.currentUser = -1

    def login(self):
        pass

    def logout(self):
        pass
