from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QFrame, QFormLayout
from PySide6.QtCore import Qt
from gestion_bdd import obtenir_details_mot, modifier_mot_bdd

class PageModifierMot(QWidget):
    def __init__(self, curseur, connexion, id_mot, retour_callback):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.curseur = curseur
        self.connexion = connexion
        self.id_mot = id_mot
        self.retour_callback = retour_callback

        main_layout = QHBoxLayout(self)

        # Sidebar
        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar_widget")
        sidebar_widget.setFixedWidth(150)
        sidebar = QVBoxLayout(sidebar_widget)
        sidebar.addWidget(QLabel("Parcourir"))
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

        instruction = QLabel("Modifier le mot :")
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

        # Style avec la couleur 86616A demandée
        style_input = """
            QLineEdit {
                color: #86616A; 
                font-size: 16px; 
                border: 1px solid #D8A4AF; 
                border-radius: 5px; 
                padding: 5px;
                background-color: transparent;
            }
        """

        labels = ["Kanji :", "Lecture :", "Traduction :", "Exemple :", "Trad. Exemple :", "Niveau :"]
        for (key, widget), txt in zip(self.inputs.items(), labels):
            lbl = QLabel(txt)
            lbl.setProperty("class", "QLabelForm")
            widget.setStyleSheet(style_input)
            widget.setMinimumWidth(300)
            widget.setFixedHeight(35)
            form_lay.addRow(lbl, widget)

        content_area.addWidget(self.card, alignment=Qt.AlignCenter)
        content_area.addStretch()

        # Bouton
        btn_mod = QPushButton("Modifier")
        btn_mod.setFixedSize(150, 45)
        btn_mod.clicked.connect(self.sauvegarder_modification)
        content_area.addWidget(btn_mod, alignment=Qt.AlignCenter)

        main_layout.addLayout(content_area)
        self.remplir_champs()

    def remplir_champs(self):
        mot = obtenir_details_mot(self.curseur, self.id_mot)
        if mot:
            self.inputs['kanji'].setText(mot[0])
            self.inputs['lecture'].setText(mot[1])
            self.inputs['traduction'].setText(mot[2])
            self.inputs['exemple'].setText(mot[3])
            self.inputs['trad_ex'].setText(mot[4])
            self.inputs['niveau'].setText(mot[5])

    def sauvegarder_modification(self):
        donnees = {k: w.text() for k, w in self.inputs.items()}
        modifier_mot_bdd(self.curseur, self.connexion, self.id_mot, donnees)
        self.retour_callback()