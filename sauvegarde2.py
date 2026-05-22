import json
import os
from src.pieces import King, Queen, Rook, Bishop, Knight, Pawn

PIECES = {"King": King, "Queen": Queen, "Rook": Rook, "Bishop": Bishop, "Knight": Knight, "Pawn": Pawn}


def save_game(chess, name="save"):
    if not os.path.exists("saves"):
        os.makedirs("saves")

    liste_pieces = []
    for pos, p in chess.board.pieces.items():
        liste_pieces.append({
            "type": type(p).__name__,
            "color": p.color,
            "pos": str(pos),
            "moved": p.has_moved
        })

    data = {
        "joueur": chess._current_index,
        "pieces": liste_pieces,
        "history": chess.history
    }

    with open(f"saves/{name}.json", "w") as f:
        json.dump(data, f, indent=4)

    print(f"Partie sauvegardée dans {name}.json")


def load_game(chess, name="save"):
    with open(f"saves/{name}.json", "r") as f:
        data = json.load(f)

    chess.board.pieces = {}

    for p_data in data["pieces"]:
        classe = PIECES[p_data["type"]]
        piece = classe(p_data["pos"], p_data["color"])
        piece.has_moved = p_data["moved"]
        chess.board.placePiece(piece, piece.position)

    chess._current_index = data["joueur"]
    chess.history = data["history"]
    print("Partie chargée !")