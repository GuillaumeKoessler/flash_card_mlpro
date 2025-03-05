import sqlite3

from src import crud_cards
from src import crud_theme
from src import stats

stats.update_stats(1)

stats.update_stats(0)

# conn = sqlite3.connect("data/flashcards.db")
# c = conn.cursor()

# c.execute(
#     """
#     INSERT INTO cards (question, reponse, probabilite, id_theme)
#     VALUES ("Je mesure quelle taille ?", "1m69", 0.5, 4)
#     """
# )
# conn.commit()
# conn.close()

stats.update_card_probability(card_id=1, is_correct=1)
stats.get_stats()
