from piece import Piece


class Knight(Piece):

    def __init__(self, position, color):

        # Initialise la position et la couleur
        super().__init__(position, color)

    def isValidMove(self, newPosition, board):

        # Position actuelle du cavalier
        start = self.position

        # Calcul du déplacement horizontal et vertical

        dx = abs(ord(newPosition.column) - ord(self.position.column))
        dy = abs(newPosition.row - self.position.row)

        # Vérifie le déplacement en L du cavalier
        valid_move = (dx == 2 and dy == 1) or (dx == 1 and dy == 2)

        # Si le mouvement n'est pas valide
        if not valid_move:
            return False

        # Récupère la pièce sur la case d'arrivée
        target_piece = board.getPiece(newPosition)

        # Empêche de manger une pièce de la même couleur
        if self.is_same_color(target_piece):
            return False

        # Sinon le déplacement est valide
        return True

    def __str__(self):


        # Cavalier noir
        return "N"