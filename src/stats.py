import sqlite3

from datetime import datetime


def update_stats(is_correct: bool) -> bool:
    """Met à jour les statistiques quotidiennes des réponses aux flashcards.

    Cette fonction incrémente soit le compteur de bonnes réponses, soit celui de mauvaises
    réponses pour la date du jour. Si aucune entrée n'existe pour aujourd'hui dans la table
    stats, une nouvelle entrée est créée.

    Args:
        is_correct (bool): True si la réponse de l'utilisateur était correcte,
                          False sinon.

    Returns:
        bool: True si la mise à jour a réussi, False en cas d'erreur.
    """
    today = datetime.now().strftime("%Y-%m-%d")

    conn = None

    try:
        conn = sqlite3.connect("data/flashcards.db")
        c = conn.cursor()

        c.execute("PRAGMA foreign_keys = ON;")

        # Recherche d'une entrée existante pour aujourd'hui
        c.execute(
            """
            SELECT 
                id,
                bonnes_reponses,
                mauvaises_reponses
            FROM
                stats
            WHERE
                date = ?
            """,
            (today,),
        )
        stats = c.fetchone()

        if stats is not None:
            # Mise à jour d'une entrée existante
            id_stats, bonnes_reponses, mauvaises_reponses = stats

            if is_correct:
                bonnes_reponses += 1
            else:
                mauvaises_reponses += 1

            c.execute(
                """
                UPDATE stats
                SET bonnes_reponses = ?, mauvaises_reponses = ?
                WHERE id = ?
                """,
                (bonnes_reponses, mauvaises_reponses, id_stats),
            )

            # Message de confirmation
            print(
                f"Stats du {today} mises à jour : {bonnes_reponses} bonnes, {mauvaises_reponses} mauvaises"
            )
        else:
            # Création d'une nouvelle entrée pour aujourd'hui
            bonnes_reponses = 1 if is_correct else 0
            mauvaises_reponses = 0 if is_correct else 1

            c.execute(
                """
                INSERT INTO stats (bonnes_reponses, mauvaises_reponses, date)
                VALUES (?, ?, ?)
                """,
                (bonnes_reponses, mauvaises_reponses, today),
            )

            # Message de confirmation
            print(
                f"Nouvelle entrée stats créée pour {today} : {bonnes_reponses} bonnes, {mauvaises_reponses} mauvaises"
            )

        conn.commit()
        return True

    except sqlite3.Error as e:
        print(f"Erreur lors de la mise à jour des statistiques : {e}")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        print(f"Erreur inattendue : {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()


def update_card_probability(card_id: int, is_correct: bool) -> bool:
    """Met à jour la probabilité d'apparition d'une carte en fonction de la réponse.

    Cette fonction ajuste la probabilité d'apparition d'une carte flashcard en la diminuant si la réponse était correcte, ou en l'augmentant si la réponse était incorrecte.
    La probabilité est toujours maintenue entre 0.1 et 1.0.

    Args:
        card_id (int): L'identifiant de la carte dont on veut ajuster la probabilité.
        is_correct (bool): True si la réponse était correcte, False sinon.

    Returns:
        bool: True si la mise à jour a réussi, False en cas d'erreur ou si la carte n'existe pas.
    """

    conn = None
    try:
        conn = sqlite3.connect("data/flashcards.db")
        c = conn.cursor()

        # Vérification de l'existence de la carte
        c.execute("SELECT COUNT(*) FROM cards WHERE id = ?", (card_id,))
        if c.fetchone()[0] == 0:
            print(f"Erreur: Aucune carte trouvée avec l'ID {card_id}")
            return False

        # Récupération de la probabilité actuelle
        c.execute(
            """
            SELECT 
                probabilite
            FROM
                cards
            WHERE
                id = ?
            """,
            (card_id,),
        )
        result = c.fetchone()

        if result is None:
            print(
                f"Erreur: Impossible de récupérer la probabilité pour la carte {card_id}"
            )
            return False

        card_prob = result[0]

        # Calcul de la nouvelle probabilité
        if is_correct:
            new_prob = card_prob * 0.9  # Diminution de la probabilité
        else:
            new_prob = card_prob * 1.1  # Augmentation de la probabilité

        # Maintenir la probabilité dans l'intervalle [0.1, 1.0]
        new_prob = max(0.1, min(new_prob, 1.0))

        # Mise à jour de la probabilité
        c.execute(
            """
            UPDATE 
                cards
            SET 
                probabilite = ?
            WHERE 
                id = ?;
            """,
            (new_prob, card_id),
        )

        # Vérifier que la mise à jour a effectivement modifié une ligne
        if c.rowcount == 0:
            print(
                f"Avertissement: Aucune modification effectuée pour la carte {card_id}"
            )
            conn.rollback()
            return False

        conn.commit()

        # Message de confirmation avec formatage amélioré
        print(
            f"Probabilité mise à jour pour la carte {card_id}: {card_prob:.3f} → {new_prob:.3f} "
            f"({'diminuée' if is_correct else 'augmentée'})"
        )

        return True

    except sqlite3.Error as e:
        print(f"Erreur SQLite lors de la mise à jour de la probabilité: {e}")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()


def get_stats() -> list:
    """Récupère toutes les statistiques de la base de données.

    Cette fonction extrait l'ensemble des stats de la table 'stats' et les retourne sous forme de liste de tuples. Chaque tuple contient l'id, le nombre de bonnes reponses, le nombre de mauvaise reponse et la date.

    Returns:
        list: Liste de tuples contenant les informations des statistiques.
              Chaque tuple a le format (id, bonnes_reponses, mauvaises_reponses, date).
              Retourne une liste vide en cas d'absence ou d'erreur.
    """
    conn = None

    try:
        conn = sqlite3.connect("data/flashcards.db")
        c = conn.cursor()

        c.execute("PRAGMA foreign_keys = ON;")

        query = """
            SELECT 
                id,
                bonnes_reponses,
                mauvaises_reponses,
                date
            FROM 
                stats
            ;
        """

        c.execute(query)
        stats = c.fetchall()

        if not stats:
            print("Information: Aucune statistique trouvée dans la base de données.")
            return []
        print(f"{len(stats)} stat(s) récupérée(s) avec succès.")
        return stats

    except sqlite3.Error as e:
        print(f"Erreur SQLite lors de la recherche des stats: {e}")
        if conn:
            conn.rollback()
        return []
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        if conn:
            conn.rollback()
        return []
    finally:
        if conn:
            conn.close()
