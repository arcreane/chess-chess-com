import os
import sys

# board.py utilise des imports "from position import ..." / "from piece import ...".
# On rend donc le dossier game/ importable.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "game"))

from board import Board, Position, WHITE, BLACK
from sources.AIplayer import AIbot
from sources.sauvegarde2 import save_game, load_game


class Chess:
    """Orchestre une partie d'echecs en mode texte."""

    def __init__(self, vs_ai=False):
        self.board = Board()
        self.vs_ai = vs_ai
        self.players = [WHITE, BLACK]
        self._current_index = 0
        self.history = []
        self.ai = AIbot() if vs_ai else None

    def current_color(self):
        return self.players[self._current_index]

    def _switch(self):
        self._current_index = 1 - self._current_index

    @staticmethod
    def _parse_case(texte):
        """'e2' -> Position('e', 2)"""
        texte = texte.strip().lower()
        colonne = texte[0]
        ligne = int(texte[1:])
        return Position(colonne, ligne)

    def play(self):
        print("=== Echecs (mode texte) ===")
        print("Coups : 'e2 e4'   |   'save nom'   |   'load nom'   |   'quit'")

        while True:
            print()
            print(self.board)

            couleur = self.current_color()

            # Fin de partie ?
            if self.board.is_checkmate(couleur):
                gagnant = BLACK if couleur == WHITE else WHITE
                print(f"Echec et mat ! {gagnant} gagne.")
                return
            if self.board.is_stalemate(couleur):
                print("Pat ! Partie nulle.")
                return
            if self.board.is_in_check(couleur):
                print("Echec !")

            # Tour de l'IA (joue les noirs)
            if self.vs_ai and couleur == BLACK:
                coup = self.ai.dec_coups(self, BLACK)
                if coup is None:
                    print("L'IA n'a aucun coup jouable.")
                    return
                piece, dest = coup
                src = piece.position
                self.board.move(piece, dest)
                self.history.append(f"{src} -> {dest}")
                print(f"IA joue {src} -> {dest}")
                self._switch()
                continue

            entree = input(f"{couleur} > ").strip()
            if not entree:
                continue

            bas = entree.lower()

            if bas == "quit":
                print("A bientot !")
                return

            if bas.startswith("save"):
                parts = entree.split()
                nom = parts[1] if len(parts) > 1 else "save"
                save_game(self, nom)
                continue

            if bas.startswith("load"):
                parts = entree.split()
                nom = parts[1] if len(parts) > 1 else "save"
                load_game(self, nom)
                continue

            parts = entree.split()
            if len(parts) != 2:
                print("Format invalide. Exemple : e2 e4")
                continue

            try:
                src = self._parse_case(parts[0])
                dst = self._parse_case(parts[1])
            except (ValueError, IndexError):
                print("Cases invalides.")
                continue

            piece = self.board.getPiece(src)
            if piece is None:
                print("Aucune piece sur cette case.")
                continue
            if piece.color != couleur:
                print("Ce n'est pas une de vos pieces.")
                continue
            if not self.board.move(piece, dst):
                print("Coup illegal.")
                continue

            self.history.append(f"{src} -> {dst}")
            self._switch()
