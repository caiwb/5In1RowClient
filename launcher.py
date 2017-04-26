# -*- encoding:utf-8 -*-

from PyQt4 import QtGui

import game_hall_widget

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    window = game_hall_widget.GameHallMainWindow()
    window.setWindowTitle(u"五子棋")
    window.show()

    sys.exit(app.exec_())