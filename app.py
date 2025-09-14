import PyQt6.QtWidgets as pq
import glob
import os
import sys
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6 import QtGui

import library.lpak as lpak

#Other function adn windows import
import settings as open_settings

# VAR
user_path = os.path.expanduser("~")+"/"
data_path = user_path+".local/share/LibreRecall"
images_dir = data_path+"/images"

program_path = "/usr/share/LibreRecall"
os.chdir(program_path)

language = "Italiano"

def show_image(image_path):
    global win
    win = pq.QWidget()
    win.setWindowTitle(lpak.get("Details", language))
    win.setWindowIcon(QtGui.QIcon('icon.png'))

    # Otteniamo dimensioni dello schermo
    screen = pq.QApplication.primaryScreen()
    screen_size = screen.availableGeometry().size()
    width, height = screen_size.width() * 0.8, screen_size.height() * 0.8  # 80% dello schermo
    win.resize(int(width), int(height))

    # Centrata
    qr = win.frameGeometry()
    cp = screen.availableGeometry().center()
    qr.moveCenter(cp)
    win.move(qr.topLeft())

    # Sfondo scuro
    win.setStyleSheet("background-color: black;")

    # Layout
    layout = pq.QVBoxLayout(win)

    # Label con immagine
    label = pq.QLabel()
    pixmap = QPixmap(image_path)
    pixmap = pixmap.scaled(
        int(width),
        int(height),
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )

    label.setPixmap(pixmap)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    layout.addWidget(label)

    win.show()

def add_images(image_list, search_term):
    global root, scroll_area, grid_layout

    # pulisco il layout
    while grid_layout.count():
        item = grid_layout.takeAt(0)
        widget = item.widget()
        if widget is not None:
            widget.setParent(None)

    row, col = 0, 0
    max_rows = 2  # numero di righe per colonna

    temp_list = image_list[::-1]  # copia della lista originale

    while temp_list:
        image = temp_list.pop(0)

        # contenitore verticale
        vbox = pq.QVBoxLayout()
        container = pq.QWidget()
        container.setLayout(vbox)

        # pulsante con immagine
        btn = pq.QPushButton()
        icon = QIcon(image)
        btn.setIcon(icon)
        btn.setIconSize(icon.actualSize(QSize(512, 512)))  # proporzionata

        policy = pq.QSizePolicy()
        policy.setHorizontalPolicy(pq.QSizePolicy.Policy.Expanding)
        policy.setVerticalPolicy(pq.QSizePolicy.Policy.Expanding)
        policy.setHeightForWidth(True)
        btn.setSizePolicy(policy)

        btn.pressed.connect(lambda image_path=image: show_image(image_path))

        # label con nome file
        raw_name = os.path.basename(image)
        name = raw_name.replace("_", " ").split(".")[0]
        label = pq.QLabel(name)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        vbox.addWidget(btn)
        vbox.addWidget(label)

        # aggiungo al layout
        grid_layout.addWidget(container, row, col)

        row += 1
        if row >= max_rows:
            row = 0
            col += 1  # passo alla colonna successiva

    if not image_list:
        if not lpak.get("No screenshots, start the daemon to begin capturing", language) == search_term:
            not_found_label = pq.QLabel(lpak.get("No images found with these words", language)+": "+search_term)
        else:
            not_found_label = pq.QLabel(search_term)
        grid_layout.addWidget(not_found_label)

def search():    
    search_term = search_bar.text()
    images_list = []
    images_data = glob.glob(f"{images_dir}/*.txt")
    for data_file in images_data:
        with open(data_file) as f:
            data = f.read()
        if search_term.lower() in data.lower():
            image_name = data_file.replace(".txt", ".png")
            images_list.append(image_name)

    add_images(images_list, search_term)


# CREA CARTELLA SE NON ESISTE
os.makedirs(images_dir, exist_ok=True)

# LISTA IMMAGINI
image_list = glob.glob(f"{images_dir}/*.png")


# GUI
app = pq.QApplication(sys.argv)
root = pq.QMainWindow()
root.setWindowTitle(lpak.get("LibreRecall", language))
root.setWindowIcon(QtGui.QIcon('icon.png'))
root.showMaximized()

central_widget = pq.QWidget()
root.setCentralWidget(central_widget)

main_layout = pq.QVBoxLayout(central_widget)

#barra di ricerca
search_layout = pq.QHBoxLayout()
search_bar = pq.QLineEdit()
search_bar.setPlaceholderText(lpak.get("Search context", language)+"...")
search_button = pq.QPushButton(lpak.get("Search", language))
search_button.pressed.connect(search)

search_layout.addWidget(search_bar)
search_layout.addWidget(search_button)

main_layout.addLayout(search_layout)

# Scroll area
scroll_area = pq.QScrollArea()
scroll_area.setWidgetResizable(True)
main_layout.addWidget(scroll_area)

# Contenuto dentro lo scroll
scroll_content = pq.QWidget()
scroll_area.setWidget(scroll_content)

# Layout a griglia per le immagini
grid_layout = pq.QGridLayout(scroll_content)

# Aggiungi immagini alla griglia
add_images(image_list, lpak.get("No screenshots, start the daemon to begin capturing", language))

#Menu bar
menu_bar = root.menuBar()
settings_menu = menu_bar.addMenu(lpak.get("Settings", language))
open_settings_option = settings_menu.addAction(lpak.get("Settings", language))
open_settings_option.triggered.connect(lambda: open_settings.settings(language))

root.show()
sys.exit(app.exec())
