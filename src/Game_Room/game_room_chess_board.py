# -*- encoding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
import game_play_manager
import logging

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
            border-image: url(res/chessboard.png);
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
        drawX = self.edge + x * self.gird - 17
        drawY = self.edge + y * self.gird - 17
        chessView = QFrame(self)
        if type == WHITE_CHESS:
            chessView.setStyleSheet('''
                QGraphicsView{
                border-image: url(res/white.png);
                background-repeat: no-repeat;
                }
                ''')
        elif type == BLACK_CHESS:
            chessView.setStyleSheet('''
                QGraphicsView{
                border-image: url(res/black.png);
                background-repeat: no-repeat;
                }
                ''')
        chessView.setGeometry(drawX, drawY, 17, 17)
        self.chessArr.append(chessView)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and \
                game_play_manager.GamePlayManager().isStarting and \
                game_play_manager.GamePlayManager().isYourTurn:
            x = round((event.pos().x() - self.edge) / self.gird)
            y = round((event.pos().y() - self.edge) / self.gird)
            game_play_manager.GamePlayManager().chess(x, y)




