from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from .page_afficher import PageAfficher  # import de la page

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Manabi - Révisions de Kanji")
        self.setGeometry(100, 100, 800, 600)

        # Gestion des pages
        self.pages = QStackedWidget()
        self.setCentralWidget(self.pages)

        # Accueil
        self.page_accueil = QWidget()
        accueil_layout = QVBoxLayout()
        self.page_accueil.setLayout(accueil_layout)

        label_accueil = QLabel("Bienvenue sur Manabi!")
        label_accueil.setAlignment(Qt.AlignCenter)
        accueil_layout.addWidget(label_accueil)

        image = QLabel()
        pixmap = QPixmap("images/logoAccueil.png")
        image.setPixmap(pixmap.scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        image.setAlignment(Qt.AlignCenter)
        accueil_layout.addWidget(image)

        # Bouton Afficher
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(30)
        buttons_layout.setAlignment(Qt.AlignCenter)
        accueil_layout.addLayout(buttons_layout)

        bouton_afficher = QPushButton("Afficher")
        bouton_afficher.setFixedSize(100, 40)
        buttons_layout.addWidget(bouton_afficher)

        # Afficher
        self.page_afficher = PageAfficher(retour_callback=lambda: self.pages.setCurrentIndex(0))

        self.pages.addWidget(self.page_accueil)
        self.pages.addWidget(self.page_afficher)

        bouton_afficher.clicked.connect(lambda: self.pages.setCurrentIndex(1))

        self.pages.setCurrentIndex(0)