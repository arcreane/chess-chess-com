import os
import sys
import pygame

def temps_partie():
    """Renvoie le temps ecoule depuis le debut, formate en MM:SS."""
    secondes = pygame.time.get_ticks() // 1000   # ms -> secondes
    minutes = secondes // 60
    return f"{minutes:02d}:{secondes % 60:02d}"
# --- Rendre le moteur (board.py + pieces) importable ---
GAME_DIR = os.path.join(os.path.dirname(__file__), "..", "game")
sys.path.insert(0, GAME_DIR)
from board import Board, Position, WHITE, BLACK  # noqa: E402

ASSETS = os.path.join(os.path.dirname(__file__), "..", "..", "assets")

# --- Geometrie ---
SQUARE = 70
BOARD_PX = SQUARE * 8          # 560
MARGIN = 40
WIN_W = BOARD_PX + 2 * MARGIN
WIN_H = BOARD_PX + 2 * MARGIN

# --- Couleurs ---
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)
SEL = (246, 246, 105)
MOVE_DOT = (90, 150, 70)
BG = (49, 46, 43)
TEXT = (235, 235, 235)
ALERT = (255, 205, 110)

COLS = "abcdefgh"

# Nom du sprite a partir du type de piece
LETTER = {"King": "K", "Queen": "Q", "Rook": "R",
          "Bishop": "B", "Knight": "N", "Pawn": "P"}


def load_sprites():
    """Charge les PNG de assets/ et les redimensionne a la taille d'une case."""
    sprites = {}
    for type_name, letter in LETTER.items():
        for color, suffix in ((WHITE, "w"), (BLACK, "b")):
            path = os.path.join(ASSETS, f"{letter}{suffix}.png")
            img = pygame.image.load(path).convert_alpha()
            sprites[(type_name, color)] = pygame.transform.smoothscale(img, (SQUARE, SQUARE))
    return sprites


def square_to_px(col_index, row):
    """col_index 0..7 (a..h), row 1..8 ; row 8 en haut, row 1 en bas (blancs en bas)."""
    x = MARGIN + col_index * SQUARE
    y = MARGIN + (8 - row) * SQUARE
    return x, y


def px_to_square(mx, my):
    """Convertit un clic en Position, ou None si hors plateau."""
    ci = (mx - MARGIN) // SQUARE
    rt = (my - MARGIN) // SQUARE
    if mx < MARGIN or my < MARGIN or ci < 0 or ci > 7 or rt < 0 or rt > 7:
        return None
    return Position(COLS[ci], 8 - rt)


def demo():
    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Echecs")
    font = pygame.font.SysFont("arial", 18)
    big = pygame.font.SysFont("arial", 26, bold=True)
    clock = pygame.time.Clock()

    sprites = load_sprites()

    board = Board()
    players = [WHITE, BLACK]
    current = 0
    selected = None     # piece selectionnee
    legal = []          # destinations legales de la piece selectionnee
    message = ""

    def color():
        return players[current]

    def maj_message():
        c = color()
        if board.is_checkmate(c):
            return f"Echec et mat ! {players[1 - current]} gagne."
        if board.is_stalemate(c):
            return "Pat ! Partie nulle."
        if board.is_in_check(c):
            return f"{c} : echec !"
        return ""

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:          # R = nouvelle partie
                    board = Board()
                    current = 0
                    selected = None
                    legal = []
                    message = ""

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = px_to_square(*event.pos)
                if pos is None:
                    continue
                piece = board.getPiece(pos)

                if selected is None:
                    if piece is not None and piece.color == color():
                        selected = piece
                        legal = board.legal_moves(piece)
                else:
                    if pos in legal:
                        board.move(selected, pos)
                        current = 1 - current
                        selected = None
                        legal = []
                        message = maj_message()
                    elif piece is not None and piece.color == color():
                        selected = piece          # on change de piece selectionnee
                        legal = board.legal_moves(piece)
                    else:
                        selected = None
                        legal = []

        # ---------- Dessin ----------
        screen.fill(BG)

        # cases
        for rt in range(8):
            for c in range(8):
                couleur = LIGHT if (rt + c) % 2 == 0 else DARK
                pygame.draw.rect(screen, couleur,
                                 pygame.Rect(MARGIN + c * SQUARE, MARGIN + rt * SQUARE, SQUARE, SQUARE))

        # surbrillance de la case selectionnee
        if selected is not None:
            ci = COLS.index(selected.position.column)
            x, y = square_to_px(ci, selected.position.row)
            pygame.draw.rect(screen, SEL, pygame.Rect(x, y, SQUARE, SQUARE))

        # coordonnees
        for i in range(8):
            t = font.render(str(8 - i), True, TEXT)
            screen.blit(t, (MARGIN // 2 - 4, MARGIN + i * SQUARE + SQUARE // 2 - 9))
            t = font.render(COLS[i].upper(), True, TEXT)
            screen.blit(t, (MARGIN + i * SQUARE + SQUARE // 2 - 5, MARGIN + BOARD_PX + 6))

        # pieces
        for (col, row), piece in board.pieces.items():
            ci = COLS.index(col)
            x, y = square_to_px(ci, row)
            sprite = sprites.get((type(piece).__name__, piece.color))
            if sprite:
                screen.blit(sprite, (x, y))

        # pastilles des coups possibles
        for dest in legal:
            ci = COLS.index(dest.column)
            x, y = square_to_px(ci, dest.row)
            pygame.draw.circle(screen, MOVE_DOT, (x + SQUARE // 2, y + SQUARE // 2), 11)

        # trait + message
        screen.blit(big.render(f"Tour des {color()}", True, TEXT), (MARGIN, 8))
        screen.blit(big.render(temps_partie(), True, TEXT), (WIN_W - 110, 8))
        if message:
            m = font.render(message, True, ALERT)
            screen.blit(m, (WIN_W - m.get_width() - MARGIN, 14))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


def run():
    demo()


if __name__ == "__main__":
    demo()
