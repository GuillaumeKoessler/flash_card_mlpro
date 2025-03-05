import sqlite3

from src import crud_cards
from src import crud_theme

crud_theme.create_theme("Slip")

crud_theme.get_theme(7)

crud_theme.update_theme(id_theme=6, theme="Calecon")

crud_theme.get_theme(6)

crud_theme.delete_theme(7)

crud_theme.get_all_themes()
