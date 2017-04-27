# -*- encoding: UTF-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
    _fromUtf8 = QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _toUtf8 = QString.toUtf8
except AttributeError:
    def _toUtf8(s):
        return s

class LoginDialog(QDialog):
    def __init__(self, parent=None, title=u'请登录'):
        QDialog.__init__(self, parent)
        desktopSize = QApplication.desktop().size()
        self.setStyleSheet("background-color: white")
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.canClose = False
        self.setWindowTitle(title)
        self.setMaximumSize(400, 300)
        self.setMinimumSize(400, 300)
        self.setWindowIcon(QIcon('res/black.png'))
        self.setGeometry((desktopSize.width() - 400) / 2,
                         (desktopSize.height() - 300) / 2 + 50, 400, 300)

        ipLbl = QLabel(self)
        ipLbl.setAlignment(Qt.AlignRight)
        ipLbl.setGeometry(70, 80, 60, 20)
        ipLbl.setText(u'服务器IP')

        portLbl = QLabel(self)
        portLbl.setAlignment(Qt.AlignRight)
        portLbl.setGeometry(70, 120, 60, 20)
        portLbl.setText(u'端口号')

        userLbl = QLabel(self)
        userLbl.setAlignment(Qt.AlignRight)
        userLbl.setGeometry(70, 160, 60, 20)
        userLbl.setText(u'账号')

        self.ipEdit = QLineEdit(self)
        self.ipEdit.setPlaceholderText('127.0.0.1')
        self.ipEdit.setFocusPolicy(Qt.ClickFocus)
        self.ipEdit.setGeometry(160, 80, 130, 20)

        self.portEdit = QLineEdit(self)
        self.portEdit.setPlaceholderText('7890')
        self.portEdit.setFocusPolicy(Qt.ClickFocus)
        self.portEdit.setGeometry(160, 120, 130, 20)

        self.userEdit = QLineEdit(self)
        self.userEdit.setGeometry(160, 160, 130, 20)

        loginBtn = QPushButton(self)
        loginBtn.setText(u'登录')
        loginBtn.clicked.connect(self.loginEvent)
        loginBtn.setGeometry(210, 220, 85, 30)

        quitBtn = QPushButton(self)
        quitBtn.setText(u'退出')
        quitBtn.clicked.connect(parent.closeWindow)
        quitBtn.setGeometry(90, 220, 85, 30)

        self.loadingLbl = QLabel(self)
        self.loadingLbl.setGeometry(80, 0, 240, 300)
        self.loadingLbl.setHidden(True)
        self.loadingLbl.setContentsMargins(10, 0, 0, 0)
        self.movie = QMovie("res/loading.gif")
        self.movie.setScaledSize(QSize(200, 200))
        self.movie.setSpeed(70)
        self.loadingLbl.setMovie(self.movie)

    def showLoading(self):
        self.loadingLbl.setHidden(False)
        self.movie.start()

    def hideLoading(self):
        self.loadingLbl.setHidden(True)
        self.movie.stop()

    def loginEvent(self):
        if not self.userEdit.text().length():
            return
        self.emit(SIGNAL("login(QString,int,QString)"),
                  self.ipEdit.text() if self.ipEdit.text().length() else '127.0.0.1',
                  self.portEdit.text().toLong() if self.portEdit.text().length() else 7890,
                  self.userEdit.text())

    def closeEvent(self, event):
        if not self.canClose:
            self.emit(SIGNAL("close"))
            event.ignore()