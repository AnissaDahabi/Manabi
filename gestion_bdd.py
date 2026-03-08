import sqlite3

def initialiser_bdd():
    connexion = sqlite3.connect("manabi.db")
    curseur = connexion.cursor()
    curseur.execute("""
    CREATE TABLE IF NOT EXISTS mots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kanji TEXT,
        lecture TEXT,
        traduction TEXT,
        exemple TEXT,
        traduction_exemple TEXT,
        niveau TEXT,
        prochaine_revision DATETIME,
        intervalle INTEGER,
        repetitions INTEGER
    )
    """)
    connexion.commit()
    connexion.close()

def afficher_mots(curseur):
    curseur.execute("SELECT id, kanji, lecture, traduction FROM mots")
    return curseur.fetchall()

def obtenir_details_mot(curseur, id_mot):
    curseur.execute(
        "SELECT kanji, lecture, traduction, exemple, traduction_exemple, niveau FROM mots WHERE id=?",
        (id_mot,)
    )
    return curseur.fetchone()

def ajouter_mot_bdd(curseur, connexion, donnees):
    curseur.execute("""
        INSERT INTO mots 
        (kanji, lecture, traduction, exemple, traduction_exemple, niveau, prochaine_revision, intervalle, repetitions)
        VALUES (?, ?, ?, ?, ?, ?, datetime('now'), 0, 0)
    """, (donnees['kanji'], donnees['lecture'], donnees['traduction'],
          donnees['exemple'], donnees['trad_ex'], donnees['niveau']))
    connexion.commit()