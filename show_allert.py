import PyQt6.QtWidgets as pq
from PyQt6.QtGui import QIcon
def show_allert(title, message):
    msg = pq.QMessageBox()
    msg.setIcon(pq.QMessageBox.Icon.Information)
    msg.setText(message)
    msg.setWindowTitle(title)
    msg.setWindowIcon(QIcon("icon.png"))
    msg.setStandardButtons(pq.QMessageBox.StandardButton.Ok | pq.QMessageBox.StandardButton.Cancel)
    retval = msg.exec()