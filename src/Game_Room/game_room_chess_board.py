from PyQt4.QtGui import *


class ChessBoard(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.setStyleSheet(
            '''
            GameRoomMain{
            border-image: url(res/chessboard.png);
            background-repeat: no-repeat;
            }
            ''')
        self.setGeometry(0, 0, 540, 540)