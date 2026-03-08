from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame, QFormLayout
from PySide6.QtCore import Qt
from gestion_bdd import ajouter_mot_bdd


class PageAjouterMot(QWidget):
    def __init__(self, curseur, connexion, retour_callback):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.curseur = curseur
        self.connexion = connexion
        self.retour_callback = retour_callback

        main_layout = QHBoxLayout(self)

        # Sidebar
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar_widget")
        sidebar_widget.setFixedWidth(150)
        sidebar = QVBoxLayout(sidebar_widget)
        sidebar.addWidget(QLabel("Parcourir"))
        for niveau in ["JLPT N5", "JLPT N4", "JLPT N3", "JLPT N2", "JLPT N1"]:
            btn = QPushButton(niveau)
            btn.setFlat(True)
            sidebar.addWidget(btn)
        sidebar.addStretch()
        main_layout.addWidget(sidebar_widget)

        content_area = QVBoxLayout()

        # Header
        header_lay = QHBoxLayout()
        btn_ret = QPushButton("Retour")
        btn_ret.setObjectName("btn_retour")
        btn_ret.setFixedSize(100, 40)
        btn_ret.clicked.connect(retour_callback)
        header_lay.addWidget(btn_ret)
        header_lay.addStretch()
        content_area.addLayout(header_lay)

        instruction = QLabel("Ajout d'un nouveau mot :")
        instruction.setObjectName("titre_page")
        instruction.setAlignment(Qt.AlignCenter)
        content_area.addWidget(instruction)

        # Card
        self.card = QFrame()
        self.card.setObjectName("card_mot_ajouter")
        form_lay = QFormLayout(self.card)
        form_lay.setSpacing(15)

        self.inputs = {
            'kanji': QLineEdit(), 'lecture': QLineEdit(), 'traduction': QLineEdit(),
            'exemple': QLineEdit(), 'trad_ex': QLineEdit(), 'niveau': QLineEdit()
        }

        labels = ["Kanji :", "Lecture :", "Traduction :", "Exemple :", "Trad. Exemple :", "Niveau :"]
        for (key, widget), txt in zip(self.inputs.items(), labels):
            lbl = QLabel(txt)
            lbl.setProperty("class", "QLabelForm")
            widget.setProperty("class", "QLineEditForm")
            widget.setMinimumWidth(300)
            widget.setFixedHeight(35)
            form_lay.addRow(lbl, widget)

        content_area.addWidget(self.card, alignment=Qt.AlignCenter)
        content_area.addStretch()

        # Bouton
        btn_aff = QPushButton("Ajouter")
        btn_aff.setFixedSize(150, 45)
        btn_aff.clicked.connect(self.sauvegarder)
        content_area.addWidget(btn_aff, alignment=Qt.AlignCenter)

        main_layout.addLayout(content_area)

    def sauvegarder(self):
        donnees = {k: w.text() for k, w in self.inputs.items()}
        ajouter_mot_bdd(self.curseur, self.connexion, donnees)
        self.retour_callback()