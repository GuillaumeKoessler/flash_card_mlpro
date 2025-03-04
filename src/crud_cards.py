import sqlite3


def create_card(question: str, reponse: str, probabilite: float, id_theme: int) -> bool:
    """
    Crée une carte dans la base de données
    """
    conn = sqlite3.connect("data/flashcards.db")
    c = conn.cursor()
    c.execute("PRAGMA foreign_keys = ON;")

    query = """
        INSERT INTO cards (question, reponse, probabilite, id_theme)
        VALUES (?, ?, ?, ?);
    """

    c.execute(query, (question, reponse, probabilite, id_theme))

    conn.commit()
    conn.close()

    return True


def get_card(id: int) -> tuple:
    """
    Récupère une carte dans la base de données
    """
    conn = sqlite3.connect("data/flashcards.db")
    c = conn.cursor()

    query = """
        SELECT 
            id,
            question,
            reponse,
            probabilite,
            id_theme
        FROM
            cards
        WHERE id = ?;
    """

    c.execute(query, (id))
    card = c.fetchone()

    conn.close()

    return card


def update_card(
    id: int, question: str, reponse: str, probabilite: float, id_theme: int
) -> bool:
    """
    Met à jour une carte dans la base de données
    """

    conn = sqlite3.connect("data/flashcards.db")
    c = conn.cursor()

    query = """
        UPDATE 
            cards
        SET
            question = ?,
            reponse = ?,
            probabilite = ?,
            id_theme = ?
        WHERE 
            id = ?;        
    """

    c.execute(query, (question, reponse, probabilite, id_theme, id))
    conn.commit()

    conn.close()

    return True


def delete_card(id: int) -> bool:
    """
    Supprime une carte dans la base de données
    """

    conn = sqlite3.connect("data/flashcards.db")
    c = conn.cursor()

    query = """
        DELETE FROM cards WHERE id = ?;
    """

    c.execute(query, (id))
    conn.commit()

    conn.close()

    return True


def get_all_cards() -> list:
    """
    Récupère toutes les cartes dans la base de données
    """
    conn = sqlite3.connect("data/flashcards.db")
    c = conn.cursor()

    query = """
        SELECT 
            id,
            question,
            reponse,
            probabilite,
            id_theme
        FROM
            cards;
    """

    c.execute(query)
    cards = c.fetchall()

    conn.close()

    return cards


def get_number_of_cards() -> int:
    """
    Permet de compter le nombre de cartes dans le base de données
    """

    conn = sqlite3.connect("data/flashcards.db")
    c = conn.cursor()

    query = """
        SELECT 
            COUNT(*) AS NB_CARDS
        FROM 
            cards;
    """

    c.execute(query)
    nb_cards = c.fetchone()

    conn.close()

    return nb_cards


def get_cards_by_theme(id_theme: int) -> list:
    """Recupère la liste des cards d'un thème choisi

    Args:
        id_theme (int): l'identifiant du thème

    Returns:
        list: liste des cards du thème
    """

    conn = sqlite3.connect("data/flashcards.db")
    c = conn.cursor()

    query = """
        SELECT 
            id,
            question,
            reponse,
            probabilite,
            id_theme
        FROM 
            cards
        WHERE 
            id_theme = ?
        ;
    """

    c.execute(query, (id_theme))

    cards = c.fetchall()

    conn.close()

    return cards
