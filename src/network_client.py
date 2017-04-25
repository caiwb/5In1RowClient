#-*- encoding: UTF-8 -*-

from netstream import netstream

class network_client(netstream):
    def __init__(self):
        netstream.__init__(self)


if __name__ == "__main__":
    network_client = network_client()
    network_client.connect('127.0.0.1', 8080)

