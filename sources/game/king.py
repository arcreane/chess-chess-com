from piece import Piece

class King(Piece):

    def isValidMove(self, newPosition, board):

        col_diff = abs(ord(newPosition.column) - ord(self.position.column) )
        row_diff = abs(newPosition.row - self.position.row )
        #le roi doit bouger tout deplacement < 0 est annulé

        if col_diff == 0 and row_diff == 0:
            return False

        #le roi doit bouger seulement de 1 case tout deplacement > 1 est annulé

        if col_diff > 1 or row_diff > 1:
            return False

        #verification si il existe une piece a l'arrivée

        target_piece = board.getPiece(newPosition)
        #impossible de manger une pièce de la meme couleur
        if self.is_same_color(target_piece):
            return False

        return True



    def __str__(self):
        return "K"
