from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem
)
from PySide6.QtCore import Qt
from gestion_bdd import afficher_mots
import os


class PageAfficher(QWidget):
    def __init__(self, curseur, retour_callback):
        super().__init__()

        self.curseur = curseur

        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        # Sidebar
        sidebar = QVBoxLayout()
        sidebar.setSpacing(10)

        label_parcourir = QLabel("Parcourir")
        sidebar.addWidget(label_parcourir)

        self.btn_niveaux = []

        for niveau in ["JLPT N5", "JLPT N4", "JLPT N3", "JLPT N2", "JLPT N1"]:
            btn = QPushButton(niveau)
            btn.setFixedHeight(30)
            btn.setFlat(True)
            btn.setStyleSheet("text-align: left; padding-left: 5px;")
            sidebar.addWidget(btn)
            self.btn_niveaux.append(btn)

        sidebar.addSpacing(20)

        label_param = QLabel("Paramètres")
        sidebar.addWidget(label_param)

        btn_param = QPushButton("Options")
        btn_param.setFixedHeight(30)
        btn_param.setFlat(True)
        btn_param.setStyleSheet("text-align: left; padding-left: 5px;")
        sidebar.addWidget(btn_param)

        sidebar.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setObjectName("sidebar_widget")
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setFixedWidth(150)

        main_layout.addWidget(sidebar_widget)

        # Contenu principal
        content_layout = QVBoxLayout()

        # Header
        header_layout = QHBoxLayout()

        self.label_title = QLabel("Liste des mots")
        header_layout.addWidget(self.label_title)

        header_layout.addStretch()

        self.bouton_ajouter = QPushButton("Ajouter")
        self.bouton_ajouter.setObjectName("bouton_ajouter")
        self.bouton_ajouter.setFixedSize(100, 40)

        header_layout.addWidget(self.bouton_ajouter)

        content_layout.addLayout(header_layout)

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Kanji", "Lecture", "Traduction"]
        )

        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 150)
        self.table.setColumnWidth(2, 150)
        self.table.setColumnWidth(3, 150)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        self.table.cellDoubleClicked.connect(self.ouvrir_page_modifier)



        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.setMinimumSize(600, 450)

        content_layout.addWidget(self.table)

        # Bouton retour
        self.btn_retour = QPushButton("Retour")
        self.btn_retour.setObjectName("btn_retour")
        self.btn_retour.setFixedSize(100, 40)
        self.btn_retour.clicked.connect(retour_callback)

        content_layout.addWidget(self.btn_retour, alignment=Qt.AlignCenter)

        content_widget = QWidget()
        content_widget.setLayout(content_layout)

        main_layout.addWidget(content_widget)

        self.charger_mots()

        self.load_qss()

    def charger_mots(self):

        mots = afficher_mots(self.curseur)

        self.table.setRowCount(len(mots))

        for row, mot in enumerate(mots):

            self.table.setItem(row, 0, QTableWidgetItem(str(mot[0])))
            self.table.setItem(row, 1, QTableWidgetItem(mot[1]))
            self.table.setItem(row, 2, QTableWidgetItem(mot[2]))
            self.table.setItem(row, 3, QTableWidgetItem(mot[3]))

    def ouvrir_page_modifier(self, row, column):

        id_mot = self.table.item(row, 0).text()

        from gui.page_afficher_mot import PageAfficherMot

        self.page_afficher_mot = PageAfficherMot(self.curseur, id_mot)

        self.page_afficher_mot.show()

    # qss
    def load_qss(self):

        qss_path = os.path.join(os.path.dirname(__file__), "styles.qss")

        if os.path.exists(qss_path):

            with open(qss_path, "r") as f:
                self.setStyleSheet(f.read())

        else:
            print("Fichier styles.qss non trouvé")