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
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.setWindowTitle(title)
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

        self.__ipEdit = QLineEdit(self)
        self.__ipEdit.setPlaceholderText('127.0.0.1')
        self.__ipEdit.setFocusPolicy(Qt.ClickFocus)
        self.__ipEdit.setGeometry(160, 80, 130, 20)

        self.__portEdit = QLineEdit(self)
        self.__portEdit.setPlaceholderText('7980')
        self.__portEdit.setFocusPolicy(Qt.ClickFocus)
        self.__portEdit.setGeometry(160, 120, 130, 20)

        self.__userEdit = QLineEdit(self)
        self.__userEdit.setGeometry(160, 160, 130, 20)

        loginBtn = QPushButton(self)
        loginBtn.setText(u'登录')
        loginBtn.clicked.connect(self.loginEvent)
        loginBtn.setGeometry(150, 220, 85, 30)

    def loginEvent(self):
        self.emit(SIGNAL("login(QString,QString,QString)"),
                  self.__ipEdit.text(),
                  self.__portEdit.text(),
                  self.__userEdit.text(),)
        self.close()

    def closeEvent(self, event):
        self.emit(SIGNAL("close"))