import os
import sys
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6 import QtGui
import PyQt6.QtWidgets as pq
import library.lpak as lpak

import sys

def settings(language):
    global status, settings_page
    user_path = os.path.expanduser("~")+"/"
    data_path = user_path+".local/share/LibreRecall"
    images_dir = data_path+"/images"
    config_path = user_path+ ".config/LibreRecall"

    if not os.path.isfile(config_path+"/service.conf"):
        with open(config_path+"/service.conf", "w") as f:
            f.write("LibreRecall_daemon=disable")

    with open(config_path+"/service.conf", "r") as f:
        data = f.readlines()
    status = data[0]
    

    def enable_disable_daemon():
        global status
        if "enable" in status:
            status = "disable"
            enable_disable_daemon_button.setText(lpak.get("enable", language))            
        else:
            status = "enable"
            enable_disable_daemon_button.setText(lpak.get("disable", language))
        
        with open(config_path+"/service.conf", "w") as f:
            f.write("LibreRecall_daemon="+status)
    

    settings_page = pq.QDialog()
    settings_page.setWindowTitle(lpak.get("LibreRecall Settings", language))
    settings_page.setGeometry(0, 0, 900, 600)   
    layout = pq.QGridLayout(settings_page)    
    settings_page.setWindowIcon(QIcon(f"icon.png"))

    settings_label = pq.QLabel(lpak.get("Settings", language))

    enable_disable_daemon_label = pq.QLabel(lpak.get("Periodic screenshots", language))
    if "enable" in status:
        button_text = lpak.get("disable", language)
    else:
        button_text = lpak.get("enable", language)
    enable_disable_daemon_button = pq.QPushButton(button_text)
    enable_disable_daemon_button.pressed.connect(lambda: enable_disable_daemon())



    layout.addWidget(settings_label, 0, 0)
    layout.addWidget(enable_disable_daemon_label, 1, 0)
    layout.addWidget(enable_disable_daemon_button, 1, 2)

    layout.setRowStretch(layout.rowCount(), 1)
    settings_page.show()



"""
app = pq.QApplication(sys.argv)
settings("Italiano")
sys.exit(app.exec())
"""
