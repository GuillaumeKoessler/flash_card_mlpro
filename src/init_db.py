import sqlite3

def init_db():
    
    # Initialises de la connexion à la base de données
    conn = sqlite3.connect('data/flashcards.db')
    c = conn.cursor()
    # On contraint la base de données sur la suppréssion d'un thème s'il est reference dans cards
    c.execute("PRAGMA foreign_keys = ON;")
    
    query_create_cards = """
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY,
            question TEXT,
            reponse TEXT,
            probabilite REAL,
            id_theme INTEGER,
            FOREIGN KEY(id_theme) REFERENCES themes(id) ON DELETE RESTRICT
        );
    """
    
    query_create_themes = """
        CREATE TABLE IF NOT EXISTS themes (
            id INTEGER PRIMARY KEY,
            theme TEXT
        );
    """
    
    query_create_stats = """
        CREATE TABLE IF NOT EXISTS stats (
            id INTEGER PRIMARY KEY,
            bonnes_reponses INTEGER,
            mauvaises_reponses INTEGER,
            date DATE
        );
    """
    
    c.execute(query_create_cards)
    c.execute(query_create_themes)
    c.execute(query_create_stats)
    
    conn.commit()
    
    query_insert_themes = """
        INSERT INTO themes (id, theme) VALUES
        (1, 'Python'),
        (2, 'SQL'),
        (3, 'Git'),
        (4, 'Machine Learning'),
        (5, 'Deep Learning'),
        (6, 'Data Visualisation');
    """
    
    c.execute(query_insert_themes)
    
    conn.commit()
    
    conn.close()    
    
if __name__ == '__main__':
    init_db()