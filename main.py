from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
import sys

app = QApplication(sys.argv)

with open("gui/styles.qss", "r") as f:
    app.setStyleSheet(f.read())

window = MainWindow()
window.show()
sys.exit(app.exec())