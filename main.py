import sqlite3

from src import crud_cards

crud_cards.create_card(
    question="Je mesure combien ?", reponse="1m69", probabilite=0.7, id_theme=4
)

crud_cards.delete_card(id=5)

test = crud_cards.get_all_cards()
