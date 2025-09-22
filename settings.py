import os
import sys
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap, QIntValidator
from PyQt6.QtCore import Qt
from PyQt6 import QtGui
import PyQt6.QtWidgets as pq
import library.lpak as lpak
from show_allert import show_allert as show_allert

import sys

def settings(language, avaible_languages):
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

    def load_settings():
        global language, images_home_number, screenshot_sleep, max_screen
        if not os.path.isfile(config_path + "/config.conf"):
            with open(config_path + "/config.conf", "w") as f:
                f.write("Language=English\n")
                f.write("Number of screens=20\n")
                f.write("Time beetween screenshot=30\n")
                f.write("Max screenshots=1000\n")
        with open(config_path + "/config.conf", "r") as f:
            data = f.readlines()
        language = data[0].split("=")[1].strip()
        images_home_number = data[1].split("=")[1].strip()
        screenshot_sleep = data[2].split("=")[1].strip()
        max_screen = data[3].split("=")[1].strip()

    

    def enable_disable_daemon():
        global status
        if "enable" in status:
            status = "disable"
            enable_disable_daemon_button.setText(lpak.get("enable", language))            
        else:
            status = "enable"
            enable_disable_daemon_button.setText(lpak.get("disable", language))
        
        

    def write_settings():
        global status, language, images_home_number, screenshot_sleep, max_screen
        new_language = menu_select_language.currentText()
        new_screen_page_number = max_screensPage_input.text()
        new_seconds_sleep = screen_interval_input.text()
        new_max_screens = max_screens_input.text()
        if new_screen_page_number == "":
            new_screen_page_number = images_home_number
        if new_seconds_sleep == "":
            new_seconds_sleep = screenshot_sleep
        if new_max_screens == "":
            new_max_screens = max_screen


        with open(config_path+"/service.conf", "w") as f:
            f.write("LibreRecall_daemon="+status)
        with open(config_path + "/config.conf", "w") as f:
            f.write("Language={}\n".format(new_language))
            f.write("Number of screens={}\n".format(new_screen_page_number))
            f.write("Time beetween screenshot={}\n".format(new_seconds_sleep))
            f.write("Max screenshots={}".format(new_max_screens))


        confirm_button.setText(lpak.get("Changed", language))

        language = new_language
        show_allert(lpak.get("Restart", language), lpak.get("Please restart LibreRecall", language))


    load_settings()
    settings_page = pq.QDialog()
    settings_page.setWindowTitle(lpak.get("LibreRecall Settings", language))
    settings_page.setGeometry(0, 0, 900, 600)   
    layout = pq.QGridLayout(settings_page)    
    settings_page.setWindowIcon(QIcon(f"icon.png"))

    settings_label = pq.QLabel(lpak.get("Settings", language))

    #Screenshot daemon
    enable_disable_daemon_label = pq.QLabel(lpak.get("Periodic screenshots", language))
    if "enable" in status:
        button_text = lpak.get("disable", language)
    else:
        button_text = lpak.get("enable", language)
    enable_disable_daemon_button = pq.QPushButton(button_text)
    enable_disable_daemon_button.pressed.connect(lambda: enable_disable_daemon())

    #Language    
    menu_select_language = pq.QComboBox()
    menu_select_language.addItems(avaible_languages)
    menu_select_language.setCurrentText(language)
    label_language=pq.QLabel(lpak.get("language", language))    

    #Select seconds
    label_interval = pq.QLabel(lpak.get("Seconds between two screenshots", language))
    screen_interval_input = pq.QLineEdit()
    screen_interval_input.setPlaceholderText(lpak.get("Maximum 3 digits allowed", language))
    screen_interval_input.setValidator(QIntValidator(1, 999))

    #Max screens number
    label_max_screens = pq.QLabel(lpak.get("Maximum number of screenshots that can be saved", language))
    max_screens_input = pq.QLineEdit()
    max_screens_input.setPlaceholderText(lpak.get("Max number", language)+": 2147483647")
    max_screens_input.setValidator(QIntValidator(1, 2147483647))

    #Screens number on page
    label_max_screensPage = pq.QLabel(lpak.get("Maximum number of screenshots that can be saved", language))
    max_screensPage_input = pq.QLineEdit()
    max_screensPage_input.setPlaceholderText(lpak.get("Max number", language)+": 2147483647")
    max_screensPage_input.setValidator(QIntValidator(1, 2147483647))

    #COnfirm button
    confirm_button = pq.QPushButton(lpak.get("Confirm changes", language))
    confirm_button.pressed.connect(write_settings)


    layout.addWidget(settings_label, 0, 0)
    layout.addWidget(enable_disable_daemon_label, 1, 0)
    layout.addWidget(enable_disable_daemon_button, 1, 1)
    layout.addWidget(label_language, 2, 0)
    layout.addWidget(menu_select_language, 2, 1)
    layout.addWidget(label_interval, 3, 0)
    layout.addWidget(screen_interval_input, 3, 1)
    layout.addWidget(label_max_screens, 4, 0)
    layout.addWidget(max_screens_input, 4, 1)
    layout.addWidget(label_max_screensPage, 5, 0)
    layout.addWidget(max_screensPage_input, 5, 1)

    layout.addWidget(confirm_button, 0, 3)

    layout.setRowStretch(layout.rowCount(), 1)
    settings_page.show()

    return settings_page



"""
app = pq.QApplication(sys.argv)
avaible_languiages = ["Italiano", "English"]
settings("Italiano", avaible_languiages)
sys.exit(app.exec())
"""
