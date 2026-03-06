from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTextEdit
)
from PySide6.QtCore import Qt
import os


class PageAfficherMot(QWidget):

    def __init__(self, curseur, id_mot):
        super().__init__()

        self.curseur = curseur
        self.id_mot = id_mot

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Sidebar

        sidebar = QVBoxLayout()

        label_parcourir = QLabel("Parcourir")
        sidebar.addWidget(label_parcourir)

        for niveau in ["JLPT N5", "JLPT N4", "JLPT N3", "JLPT N2", "JLPT N1"]:
            btn = QPushButton(niveau)
            btn.setFixedHeight(30)
            btn.setFlat(True)
            btn.setStyleSheet("text-align: left; padding-left: 5px;")
            sidebar.addWidget(btn)

        sidebar.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar_widget")
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setFixedWidth(150)

        main_layout.addWidget(sidebar_widget)

        # Contenu principal

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)

        # Card

        self.card = QWidget()
        self.card.setObjectName("card_mot")

        card_layout = QVBoxLayout()
        card_layout.setAlignment(Qt.AlignCenter)
        card_layout.setSpacing(15)

        self.card.setLayout(card_layout)

        # ID
        self.label_id = QLabel()
        self.label_id.setObjectName("mot_id")

        # Kanji
        self.label_kanji = QLabel()
        self.label_kanji.setObjectName("kanji_label")
        self.label_kanji.setAlignment(Qt.AlignCenter)

        # Lecture - Traduction
        self.label_lecture_trad = QLabel()
        self.label_lecture_trad.setObjectName("lecture_trad")
        self.label_lecture_trad.setAlignment(Qt.AlignCenter)

        # Exemple
        self.label_exemple = QTextEdit()
        self.label_exemple.setObjectName("exemple")
        self.label_exemple.setReadOnly(True)
        self.label_exemple.setAlignment(Qt.AlignCenter)
        self.label_exemple.setFixedHeight(60)

        # Traduction exemple
        self.label_trad_exemple = QTextEdit()
        self.label_trad_exemple.setObjectName("trad_exemple")
        self.label_trad_exemple.setReadOnly(True)
        self.label_trad_exemple.setAlignment(Qt.AlignCenter)
        self.label_trad_exemple.setFixedHeight(60)


        # Niveau
        self.label_niveau = QLabel()
        self.label_niveau.setObjectName("niveau_label")
        self.label_niveau.setAlignment(Qt.AlignCenter)
        self.label_niveau.setAlignment(Qt.AlignCenter)

        card_layout.addWidget(self.label_id, alignment=Qt.AlignLeft)

        card_layout.addWidget(self.label_kanji, alignment=Qt.AlignCenter)
        card_layout.addWidget(self.label_lecture_trad, alignment=Qt.AlignCenter)
        card_layout.addWidget(self.label_exemple, alignment=Qt.AlignCenter)
        card_layout.addWidget(self.label_trad_exemple, alignment=Qt.AlignCenter)
        card_layout.addWidget(self.label_niveau, alignment=Qt.AlignCenter)

        content_layout.addWidget(self.card)

        # Boutons

        boutons_layout = QHBoxLayout()

        self.btn_modifier = QPushButton("Modifier")
        self.btn_supprimer = QPushButton("Supprimer")

        boutons_layout.addWidget(self.btn_modifier)
        boutons_layout.addWidget(self.btn_supprimer)

        content_layout.addLayout(boutons_layout)

        main_layout.addLayout(content_layout)

        self.charger_mot()
        self.load_qss()

    def charger_mot(self):

        self.curseur.execute(
            "SELECT kanji, lecture, traduction, exemple, traduction_exemple, niveau FROM mots WHERE id=?",
            (self.id_mot,)
        )

        mot = self.curseur.fetchone()

        if mot:

            self.label_id.setText(f"ID : {self.id_mot}")
            self.label_kanji.setText(mot[0])
            self.label_lecture_trad.setText(f"{mot[1]}  -  {mot[2]}")
            self.label_exemple.setText(mot[3])
            self.label_trad_exemple.setText(mot[4])
            self.label_niveau.setText(f"Niveau : {mot[5]}")

    def load_qss(self):

        qss_path = os.path.join(os.path.dirname(__file__), "styles.qss")

        if os.path.exists(qss_path):

            with open(qss_path, "r") as f:
                self.setStyleSheet(f.read())