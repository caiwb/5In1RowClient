# -*- encoding: UTF-8 -*-

from src.Model.user_model import UserModel

class RoomModel(object):
    def __init__(self, dict):
        self.roomId = dict['rid']
        userList = dict['users']
        self.users = []
        for ud in userList:
            user = UserModel(ud)
            self.users.append(user)

