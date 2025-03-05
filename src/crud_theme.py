import sqlite3


def create_theme(theme: str) -> bool:
    """
    Insert une valeur dans la table des themes
    """

    conn = sqlite3.connect("data/flashcards.db")
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    query = """
        INSERT INTO themes (theme)
        VALUES (?);
    """

    c.execute(query, (theme,))
    conn.commit()

    conn.close()

    return True


def get_theme(id_theme: int) -> tuple:
    """Recupere le nom du theme selon son id

    Args:
        id_theme (int): id du theme recherché

    Returns:
        tuple: tuple contenant l'id et le nom du thème
    """

    conn = sqlite3.connect("data/flashcards.db")
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    query = """
        SELECT 
            id,
            theme
        FROM 
            themes
        WHERE 
            id = ?;
    """

    c.execute(query, (id_theme,))
    theme = c.fetchone()
    conn.commit()

    conn.close()

    return theme


def update_theme(id_theme: int, theme: str) -> bool:
    """Met à jour un thème selon son id

    Args:
        id_theme (int): id du thème à mettre à jour
        theme (str): nom du nouveau theme

    Returns:
        bool: Renvoi True si la fonction à fonctionné
    """
    conn = sqlite3.connect("data/flashcards.db")
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    query = """
        UPDATE 
            themes
        SET
            theme = ?
        WHERE 
            id = ?;
    """

    c.execute(query, (theme, id_theme))
    conn.commit()

    conn.close()

    return True


def delete_theme(id_theme: int) -> bool:
    """Permet de supprimer un theme par rapport à son id

    Args:
        id_theme (int): id du theme a supprimer

    Returns:
        bool: True si success de la fonction
    """

    conn = sqlite3.connect("data/flashcards.db")
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    query = """
        DELETE FROM themes
        WHERE id = ?;
    """

    c.execute(query, (id_theme,))
    conn.commit()

    conn.close()

    return True


def get_all_themes() -> list:
    """Retourne l'ensemble des lignes de la table themes dans une liste

    Returns:
        list: liste des themes
    """

    conn = sqlite3.connect("data/flashcards.db")
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    query = """
        SELECT 
            id,
            theme
        FROM 
            themes
        ;
    """

    c.execute(query)
    themes = c.fetchall()

    conn.close()

    return themes
