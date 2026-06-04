from piece import Piece

class Bishop(Piece):

    def isValidMove(self, newPosition, board):
        current_col = ord(self.position.column)
        current_row = self.position.row
        new_col = ord(newPosition.column)
        new_row = newPosition.row

        col_diff = new_col - current_col
        row_diff = new_row - current_row

        if col_diff == 0 and row_diff == 0:
            return False

        is_diagonal = abs(col_diff) == abs(row_diff)  #valeur absolu

        if not is_diagonal:
            return False

        step_col = 1 if col_diff > 0 else -1
        step_row = 1 if row_diff > 0 else -1

        check_col = current_col + step_col
        check_row = current_row + step_row

        while check_col != new_col or check_row != new_row:
            intermediate_position = type(self.position)(chr(check_col), check_row)

            if board.getPiece(intermediate_position) is not None:
                return False

            check_col += step_col
            check_row += step_row

        target_piece = board.getPiece(newPosition)

        if self.is_same_color(target_piece):
            return False

        return True

    def __str__(self):
        return "B"



