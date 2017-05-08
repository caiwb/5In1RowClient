# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from src.Networking import game_play_manager

#chess
NONE_CHESS  = 0
WHITE_CHESS = 1
BLACK_CHESS = 2

class ChessBoard(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.parent = parent
        self.setStyleSheet(
            '''
            ChessBoard{
            border-image: url(:chessboard);
            background-repeat: no-repeat;
            }
            ''')
        self.setGeometry(15, 15, 500, 500)
        self.start = False
        self.connect(game_play_manager.GamePlayManager(), SIGNAL("start"),
                     self.startGame)
        self.connect(game_play_manager.GamePlayManager(),
                     SIGNAL("chess(int,int,int)"), self.drawChess)
        self.edge = self.width() * 0.042
        self.gird = (self.width() - self.edge * 2) / 14
        self.chessArr = []

    def startGame(self):
        pass

    def drawChess(self, x, y, type):
        drawX = self.edge + x * self.gird - 15
        drawY = self.edge + y * self.gird - 15
        self.chessView = QFrame(self)
        if type == WHITE_CHESS:
            self.chessView.setStyleSheet('''
                border-image: url(:white);
                background-repeat: no-repeat;
                ''')
        elif type == BLACK_CHESS:
            self.chessView.setStyleSheet('''
                border-image: url(:black);
                background-repeat: no-repeat;
                ''')
        self.chessView.setGeometry(drawX, drawY, 30, 30)
        self.chessView.setMinimumSize(30, 30)
        self.chessArr.append(self.chessView)
        self.chessView.show()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and \
                game_play_manager.GamePlayManager().isStarting and \
                game_play_manager.GamePlayManager().isYourTurn:
            x = int(round((event.pos().x() - self.edge) / self.gird))
            y = int(round((event.pos().y() - self.edge) / self.gird))
            game_play_manager.GamePlayManager().chess(x, y)

    def clear(self):
        for i in range(len(self.chessArr)):
            chess = self.chessArr[i]
            chess.close()
        self.chessArr = []

    def redo(self, step):
        while step:
            chess = self.chessArr.pop()
            chess.close()
            step -= 1


