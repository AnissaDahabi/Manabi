from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
import sqlite3
import sys

connexion = sqlite3.connect("manabi.db")
curseur = connexion.cursor()

app = QApplication(sys.argv)

with open("gui/styles.qss", "r") as f:
    app.setStyleSheet(f.read())

window = MainWindow(curseur)
window.show()
sys.exit(app.exec())