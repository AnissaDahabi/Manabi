from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QAbstractItemView, QHeaderView
)
from PySide6.QtCore import Qt
from gestion_bdd import afficher_mots


class PageAfficher(QWidget):
    def __init__(self, curseur, stacked_widget, retour_callback):
        super().__init__()
        self.curseur = curseur
        self.stacked_widget = stacked_widget

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

        content_layout = QVBoxLayout()
        content_layout.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()
        self.btn_retour = QPushButton("Retour")
        self.btn_retour.setObjectName("btn_retour")
        self.btn_retour.setFixedSize(100, 40)
        self.btn_retour.setCursor(Qt.PointingHandCursor)
        self.btn_retour.clicked.connect(retour_callback)
        header_layout.addWidget(self.btn_retour)
        header_layout.addStretch()
        content_layout.addLayout(header_layout)

        self.label_titre = QLabel("Liste des mots")
        self.label_titre.setObjectName("titre_page")
        self.label_titre.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.label_titre)

        # Tableau
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Kanji", "Lecture", "Traduction"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setFocusPolicy(Qt.NoFocus)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.cellDoubleClicked.connect(self.ouvrir_page_details)
        content_layout.addWidget(self.table)

        # Footer
        footer_layout = QHBoxLayout()
        self.btn_ajouter = QPushButton("Ajouter")
        self.btn_ajouter.setFixedSize(150, 45)
        self.btn_ajouter.setCursor(Qt.PointingHandCursor)
        self.btn_ajouter.clicked.connect(self.ouvrir_page_ajouter)
        footer_layout.addStretch()
        footer_layout.addWidget(self.btn_ajouter)
        footer_layout.addStretch()
        footer_layout.setContentsMargins(0, 0, 0, 20)
        content_layout.addLayout(footer_layout)

        main_layout.addLayout(content_layout)
        self.charger_mots()

    def charger_mots(self):
        mots = afficher_mots(self.curseur)
        self.table.setRowCount(len(mots))
        for row, mot in enumerate(mots):
            for col in range(4):
                item = QTableWidgetItem(str(mot[col]))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row, col, item)

    def ouvrir_page_details(self, row, column):
        id_mot = self.table.item(row, 0).text()
        from .page_afficher_mot import PageAfficherMot

        def retour_et_reload():
            self.stacked_widget.setCurrentIndex(1)
            self.charger_mots()

        self.page_detail = PageAfficherMot(self.curseur, id_mot, retour_et_reload)
        self.stacked_widget.addWidget(self.page_detail)
        self.stacked_widget.setCurrentWidget(self.page_detail)

    def ouvrir_page_ajouter(self):
        from .page_ajouter_mot import PageAjouterMot
        connexion = self.curseur.connection

        def retour_et_reload():
            self.stacked_widget.setCurrentIndex(1)
            self.charger_mots()

        self.page_ajouter = PageAjouterMot(self.curseur, connexion, retour_et_reload)
        self.stacked_widget.addWidget(self.page_ajouter)
        self.stacked_widget.setCurrentWidget(self.page_ajouter)