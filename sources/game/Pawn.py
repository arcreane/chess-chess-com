from piece import Piece

WHITE = "white"
BLACK = "black"


class Pawn(Piece):

    def isValidMove(self, newPosition, board):
        col_diff = ord(newPosition.column) - ord(self.position.column)
        row_diff = newPosition.row - self.position.row

        # Blanc monte (row 2 -> 8), noir descend (row 7 -> 1)
        direction = 1 if self.color == WHITE else -1
        start_row = 2 if self.color == WHITE else 7

        target_piece = board.getPiece(newPosition)

        # Avance simple
        if col_diff == 0 and row_diff == direction and target_piece is None:
            return True

        # Premier coup de 2 cases (la case intermediaire doit etre libre)
        if col_diff == 0 and row_diff == 2 * direction and self.position.row == start_row:
            intermediate = type(self.position)(self.position.column, self.position.row + direction)
            if target_piece is None and board.getPiece(intermediate) is None:
                return True

        # Capture en diagonale
        if abs(col_diff) == 1 and row_diff == direction:
            if target_piece is not None and not self.is_same_color(target_piece):
                return True

        return False

    def __str__(self):
        return "P"
