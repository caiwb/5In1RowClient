# -*- encoding: UTF-8 -*-

class UserModel(object):
    def __init__(self, dict):
        self.uid = dict['uid']
        self.account = dict['account']
        self.score = dict['score']
