from piece import Piece


class Pawn(Piece):

    def __init__(self, position, color):

        # Initialise la position et la couleur
        super().__init__(position, color)

    def isValidMove(self, newPosition, board):

        # Position actuelle du pion
        start = self.position

        # Différence de déplacement
        dx = newPosition[0] - start[0]
        dy = newPosition[1] - start[1]

        # Direction du pion
        # Blanc monte, noir descend
        if self.color == 0:
            direction = 1
        else:
            direction = -1

        # Vérifie si une pièce est sur la case d'arrivée
        target_piece = board.getPiece(newPosition)

        # Déplacement simple vers l'avant
        if dx == 0 and dy == direction and target_piece is None:
            return True

        # Premier déplacement de 2 cases
        if dx == 0 and dy == 2 * direction and target_piece is None:

            # Position de départ des pions
            if (self.color == 0 and start[1] == 1) or (self.color == 1 and start[1] == 6):
                return True

        # Capture en diagonale
        if abs(dx) == 1 and dy == direction:

            # Vérifie qu'il y a une pièce ennemie
            if target_piece is not None and not self.is_same_color(target_piece):
                return True

        # Sinon mouvement invalide
        return False

    def __str__(self):

        # Pion blanc
        if self.color == 0:
            return "P"

        # Pion noir
        return "p"