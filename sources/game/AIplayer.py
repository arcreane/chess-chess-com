import random


class AIbot:
    def __init__(self, name="bot"):
        # Constructeur de la classe
        # name est le nom du bot, avec "bot" comme valeur par défaut
        self.name = name

    def dec_coups(self, chess, color):
        """
        Cette méthode décide d'un coup à jouer.
        Elle renvoie un tuple (piece, destination),
        ou None s'il n'y a aucun coup légal possible.
        """

        coups = []  # Liste qui va contenir tous les coups possibles

        # On parcourt toutes les pièces du joueur (couleur donnée)
        for piece in chess.board.all_pieces_of(color):

            # Pour chaque pièce, on récupère tous ses coups légaux
            for dest in chess.board.legal_moves(piece):

                # On ajoute le coup sous forme de tuple (piece, destination)
                coups.append((piece, dest))

        # Si aucun coup n’est disponible (ex: échec et mat ou pat)
        if not coups:
            return None

        # Sinon, on choisit un coup au hasard dans la liste
        return random.choice(coups)