import os
import sys
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6 import QtGui

import library.lpak as lpak


def settings(language):
    def enable_disable_daemon():
        pass

    settings_page = pq.QDialog()
    settings_page.setWindowTitle(lpak.get("LibreRecall Settings", language))
    settings_page.setGeometry(0, 0, 900, 600)   
    layout = pq.QGridLayout(settings_page)    
    settings_page.setWindowIcon(QIcon(f"icon.png"))


    enable_disable_daemon_label = pq.QLabel(lpak.get("Periodic screenshots", language))
    enable_disable_daemon_button = pq.QPushButton

