# -*- encoding:utf-8 -*-

from PyQt4 import QtGui

import game_hall_widget
import sys
import logging

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] '
                               '- %(levelname)s: %(message)s')
    app = QtGui.QApplication(sys.argv)
    window = game_hall_widget.GameHallMainWindow()
    window.setWindowTitle(u"五子棋")
    window.show()

    sys.exit(app.exec_())