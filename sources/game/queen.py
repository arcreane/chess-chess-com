from piece import Piece


class Queen(Piece):

    def isValidMove(self, newPosition, board):

#on convertie les colonne qui sont des lettres en chiffre et on definit les variables des col/ligne precédentes et nouvelles
        current_col = ord(self.position.column)
        current_row = self.position.row
        new_col = ord(newPosition.column)
        new_row = newPosition.row


        col_diff = new_col - current_col
        row_diff = new_row - current_row

        # la reine doit bouger tout deplacement < 0 est annulé

        if col_diff == 0 and row_diff == 0:
            return False

        #on définit le type de déplacement : soit en ligne soit en diagonal

        is_straight = (col_diff == 0 or row_diff == 0)
        is_diagonal = abs(col_diff) == abs(row_diff)

        if not (is_straight or is_diagonal):
            return False

        step_col = 0 if col_diff == 0 else (1 if col_diff > 0 else -1)
        step_row = 0 if row_diff == 0 else (1 if row_diff > 0 else -1)

        check_col = current_col + step_col
        check_row = current_row + step_row

        while check_col !=  new_col or check_row != new_row:
            intermediate_position = type(self.position)(chr(check_col), check_row)

            if board.getPiece(intermediate_position) is not None:
                return False

            check_col += step_col
            check_row += step_row

    # verification si il existe une piece a l'arrivée

        target_piece = board.getPiece(newPosition)
        # impossible de manger une pièce de la meme couleur
        if self.is_same_color(target_piece):
            return False

        return True

    def __str__(self):
        return "Q"