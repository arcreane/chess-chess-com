from position import Position

WHITE = "white"
BLACK = "black"
COLS = "abcdefgh"

class Board:
    def __init__(self):
        self.pieces = {}
        self._setup()

    def _setup(self):
        from piece import King, Queen, Rook, Bishop, Knight, Pawn
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for ci, cls in enumerate(order):
            col = COLS[ci]
            self.place(cls(Position(col, 1), WHITE))
            self.place(cls(Position(col, 8), BLACK))
        for col in COLS:
            self.place(Pawn(Position(col, 2), WHITE))
            self.place(Pawn(Position(col, 7), BLACK))

    def place(self, piece):
        self.pieces[(piece.position.column, piece.position.row)] = piece

    def get(self, pos):
        return self.pieces.get((pos.column, pos.row))
    def getPiece(self, pos):
        return self.get(pos)

    def remove(self, pos):
        self.pieces.pop((pos.column, pos.row), None)

    def _all_positions(self):
        return [Position(col, row) for col in COLS for row in range(1, 9)]

    def legal_moves(self, piece):
        return [
            dest for dest in self._all_positions()
            if piece.isValidMove(dest, self)
            and not self._leaves_in_check(piece, dest)
        ]

    def _leaves_in_check(self, piece, dest):
        saved_pieces = dict(self.pieces)
        old_pos = piece.position

        self.remove(old_pos)
        self.pieces[(dest.column, dest.row)] = piece
        piece.position = dest

        in_check = self.is_in_check(piece.color)

        self.pieces = saved_pieces
        piece.position = old_pos
        return in_check

    def move(self, piece, dest):
        if dest not in self.legal_moves(piece):
            return False

        from piece import Pawn, King, Rook, Queen

        src = piece.position
        ci_src = COLS.index(src.column)
        ci_dst = COLS.index(dest.column)

        if isinstance(piece, King) and abs(ci_dst - ci_src) == 2:
            ri = src.row
            if ci_dst == 6:
                rook = self.get(Position(COLS[7], ri))
                self.remove(Position(COLS[7], ri))
                new_rook_pos = Position(COLS[5], ri)
            else:
                rook = self.get(Position(COLS[0], ri))
                self.remove(Position(COLS[0], ri))
                new_rook_pos = Position(COLS[3], ri)
            rook.move_to(new_rook_pos)
            if hasattr(rook, 'has_moved'):
                rook.has_moved = True
            self.pieces[(new_rook_pos.column, new_rook_pos.row)] = rook

        self.remove(src)
        piece.move_to(dest)
        if hasattr(piece, 'has_moved'):
            piece.has_moved = True
        self.pieces[(dest.column, dest.row)] = piece

        if isinstance(piece, Pawn):
            if (piece.color == WHITE and dest.row == 8) or \
               (piece.color == BLACK and dest.row == 1):
                queen = Queen(dest, piece.color)
                if hasattr(queen, 'has_moved'):
                    queen.has_moved = True
                self.pieces[(dest.column, dest.row)] = queen

        return True

    def find_king(self, color):
        from piece import King
        for key, piece in self.pieces.items():
            if isinstance(piece, King) and piece.color == color:
                return piece.position
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if king_pos is None:
            return False
        opponent = BLACK if color == WHITE else WHITE
        for piece in list(self.pieces.values()):
            if piece.color == opponent:
                if piece.isValidMove(king_pos, self):
                    return True
        return False

    def has_any_legal_move(self, color):
        for piece in list(self.pieces.values()):
            if piece.color == color and self.legal_moves(piece):
                return True
        return False

    def is_checkmate(self, color):
        return self.is_in_check(color) and not self.has_any_legal_move(color)

    def is_stalemate(self, color):
        return not self.is_in_check(color) and not self.has_any_legal_move(color)

    def all_pieces_of(self, color):
        return [p for p in self.pieces.values() if p.color == color]

    def __str__(self):
        rows = []
        for row in range(8, 0, -1):
            line = f"{row} "
            for col in COLS:
                pos = Position(col, row)
                piece = self.get(pos)
                line += (str(piece) if piece else "·") + " "
            rows.append(line)
        rows.append("  a b c d e f g h")
        return "\n".join(rows)