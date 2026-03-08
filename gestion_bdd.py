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


def modifier_mot_bdd(curseur, connexion, id_mot, donnees):
    curseur.execute("SELECT * FROM mots WHERE id=?", (id_mot,))
    ancien = curseur.fetchone()

    colonnes = ["kanji", "lecture", "traduction", "exemple", "traduction_exemple", "niveau"]
    valeurs_finales = []

    cles_donnees = ['kanji', 'lecture', 'traduction', 'exemple', 'trad_ex', 'niveau']

    for i, cle in enumerate(cles_donnees):
        nouvelle_valeur = donnees[cle].strip()
        valeurs_finales.append(nouvelle_valeur if nouvelle_valeur else ancien[i + 1])

    query = """
        UPDATE mots 
        SET kanji=?, lecture=?, traduction=?, exemple=?, traduction_exemple=?, niveau=?
        WHERE id=?
    """
    curseur.execute(query, (*valeurs_finales, id_mot))
    connexion.commit()

def supprimer_mot_bdd(curseur, connexion, id_mot):
    curseur.execute("DELETE FROM mots WHERE id = ?", (id_mot,))
    connexion.commit()