from PyQt4.QtGui import *


class ChessBoard(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.setStyleSheet(
            '''
            ChessBoard{
            border-image: url(res/chessboard.png);
            background-repeat: no-repeat;
            }
            ''')
        self.setGeometry(15, 15, 500, 500)

