"""
board.py — Classe Board pour un échiquier Python
Dépend de : Position, Piece et ses sous-classes (piece.py)
"""

WHITE = "white"
BLACK = "black"
COLS = "abcdefgh"


class Board:
    """
    Plateau de jeu.

    Attributs :
        pieces          dict[Position, Piece]  — état courant du plateau
        en_passant_target  Position | None     — cible de prise en passant
    """

    def __init__(self):
        self.pieces: dict = {}
        self.en_passant_target = None
        self._setup()

    # ── Mise en place ────────────────────────
    def _setup(self):
        """Place toutes les pièces en position initiale."""
        from piece import (King, Queen, Rook, Bishop, Knight, Pawn, Position)
        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for ci, cls in enumerate(order):
            col = COLS[ci]
            self.place(cls(WHITE, Position(col, 1)))
            self.place(cls(BLACK, Position(col, 8)))
        for col in COLS:
            self.place(Pawn(WHITE, Position(col, 2)))
            self.place(Pawn(BLACK, Position(col, 7)))

    # ── CRUD pièces ──────────────────────────
    def place(self, piece):
        """Place une pièce sur le plateau."""
        self.pieces[piece.position] = piece

    def get(self, pos):
        """Retourne la pièce à la position donnée, ou None."""
        return self.pieces.get(pos)

    def remove(self, pos):
        """Retire la pièce à la position donnée."""
        self.pieces.pop(pos, None)

    # ── Mouvements légaux ────────────────────
    def legal_moves(self, piece) -> list:
        """
        Retourne la liste des destinations légales pour une pièce.
        Filtre les coups pseudo-légaux qui laisseraient le roi en échec.
        """
        return [dest for dest in piece.pseudo_legal_moves(self)
                if not self._leaves_in_check(piece, dest)]

    def _leaves_in_check(self, piece, dest) -> bool:
        """Simule le coup et vérifie si le roi est en échec après."""
        saved_pieces = dict(self.pieces)
        saved_ep = self.en_passant_target

        # Prise en passant : retirer le pion capturé
        from piece import Pawn
        if isinstance(piece, Pawn) and dest == self.en_passant_target:
            direction = 1 if piece.color == WHITE else -1
            ep_ci, ep_ri = dest.to_indices()
            from piece import Position
            ep_pawn_pos = Position.from_indices(ep_ci, ep_ri - direction)
            self.remove(ep_pawn_pos)

        self.remove(piece.position)
        self.pieces[dest] = piece
        old_pos = piece.position
        piece.position = dest

        in_check = self.is_in_check(piece.color)

        # Restauration
        self.pieces = saved_pieces
        piece.position = old_pos
        self.en_passant_target = saved_ep
        return in_check

    def move(self, piece, dest) -> bool:
        """
        Effectue un coup légal.
        Gère : roque, prise en passant, promotion automatique en Dame.
        Retourne True si le coup a été joué, False sinon.
        """
        if dest not in self.legal_moves(piece):
            return False

        from piece import Pawn, King, Rook, Queen, Position
        src = piece.position
        ci_src, ri_src = src.to_indices()
        ci_dst, ri_dst = dest.to_indices()

        # Réinitialise la cible en passant
        self.en_passant_target = None

        # Prise en passant
        if isinstance(piece, Pawn) and dest == self.en_passant_target:
            direction = 1 if piece.color == WHITE else -1
            ep_ci, ep_ri = dest.to_indices()
            self.remove(Position.from_indices(ep_ci, ep_ri - direction))

        # Double avance du pion → active la cible en passant
        if isinstance(piece, Pawn) and abs(ri_dst - ri_src) == 2:
            mid_ri = (ri_src + ri_dst) // 2
            self.en_passant_target = Position.from_indices(ci_src, mid_ri)

        # Roque
        if isinstance(piece, King) and abs(ci_dst - ci_src) == 2:
            ri = ri_src
            if ci_dst == 6:   # petit roque
                rook = self.get(Position.from_indices(7, ri))
                self.remove(Position.from_indices(7, ri))
                new_pos = Position.from_indices(5, ri)
            else:             # grand roque
                rook = self.get(Position.from_indices(0, ri))
                self.remove(Position.from_indices(0, ri))
                new_pos = Position.from_indices(3, ri)
            rook.position = new_pos
            rook.has_moved = True
            self.pieces[new_pos] = rook

        # Déplacement principal
        self.remove(src)
        piece.position = dest
        piece.has_moved = True
        self.pieces[dest] = piece

        # Promotion du pion (automatique en Dame)
        if isinstance(piece, Pawn):
            if (piece.color == WHITE and ri_dst == 7) or \
               (piece.color == BLACK and ri_dst == 0):
                queen = Queen(piece.color, dest)
                queen.has_moved = True
                self.pieces[dest] = queen

        return True

    # ── État de la partie ────────────────────
    def find_king(self, color):
        """Retourne la Position du roi de la couleur donnée, ou None."""
        from piece import King
        for pos, piece in self.pieces.items():
            if isinstance(piece, King) and piece.color == color:
                return pos
        return None

    def is_in_check(self, color) -> bool:
        """Retourne True si le roi de cette couleur est en échec."""
        king_pos = self.find_king(color)
        if king_pos is None:
            return False
        opponent = BLACK if color == WHITE else WHITE
        for piece in list(self.pieces.values()):
            if piece.color == opponent:
                if king_pos in piece.pseudo_legal_moves(self):
                    return True
        return False

    def has_any_legal_move(self, color) -> bool:
        """Retourne True si la couleur a au moins un coup légal."""
        for piece in list(self.pieces.values()):
            if piece.color == color and self.legal_moves(piece):
                return True
        return False

    def is_checkmate(self, color) -> bool:
        """Retourne True si la couleur est en échec et mat."""
        return self.is_in_check(color) and not self.has_any_legal_move(color)

    def is_stalemate(self, color) -> bool:
        """Retourne True si la couleur est en pat."""
        return not self.is_in_check(color) and not self.has_any_legal_move(color)

    def all_pieces_of(self, color) -> list:
        """Retourne toutes les pièces d'une couleur."""
        return [p for p in self.pieces.values() if p.color == color]

    # ── Affichage texte ──────────────────────
    def __str__(self) -> str:
        rows = []
        for ri in range(7, -1, -1):
            row = f"{ri + 1} "
            for ci in range(8):
                from piece import Position
                pos = Position.from_indices(ci, ri)
                piece = self.get(pos)
                row += (piece.symbol() if piece else "·") + " "
            rows.append(row)
        rows.append("  a b c d e f g h")
        return "\n".join(rows)