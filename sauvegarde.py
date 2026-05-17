import json
import os
from pathlib import Path

from src.position import Position
from src.piece import Piece
from src.pieces import King, Queen, Rook, Bishop, Knight, Pawn
from src.board import Board


SAVE_DIR = Path("saves")


PIECE_CLASSES = {
    "King": King,
    "Queen": Queen,
    "Rook": Rook,
    "Bishop": Bishop,
    "Knight": Knight,
    "Pawn": Pawn,
}



def save_game(chess, filename: str = "save") -> str:

    SAVE_DIR.mkdir(exist_ok=True)
    filepath = SAVE_DIR / f"{filename}.json"

    data = {
        "current_player": chess._current_index,
        "vs_ai": chess._vs_ai,
        "history": chess.history,
        "pieces": _serialize_pieces(chess.board),
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return str(filepath)


def _serialize_pieces(board: Board) -> list[dict]:
    result = []
    for position, piece in board.pieces.items():
        result.append({
            "type": type(piece).__name__,
            "color": piece.color,
            "position": str(position),
            "has_moved": piece.has_moved,
        })
    return result


def load_game(chess, filename: str = "save") -> None:

    filepath = SAVE_DIR / f"{filename}.json"
    if not filepath.exists():
        raise FileNotFoundError(f"Sauvegarde introuvable : {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    new_board = Board(empty=True)
    for entry in data["pieces"]:
        piece = _deserialize_piece(entry)
        new_board.placePiece(piece, piece.position)

        piece._has_moved = entry.get("has_moved", False)


    chess._board = new_board
    chess._current_index = data.get("current_player", 0)
    chess._vs_ai = data.get("vs_ai", False)
    chess._move_history = list(data.get("history", []))

    chess.initPlayers(chess._vs_ai)
    if chess._vs_ai and hasattr(chess.players[1], "setBoard"):
        chess.players[1].setBoard(new_board)


def _deserialize_piece(entry: dict) -> Piece:

    PieceClass = PIECE_CLASSES.get(entry["type"])
    if PieceClass is None:
        raise ValueError(f"Type de pièce inconnu : {entry['type']}")
    position = Position.from_string(entry["position"])
    return PieceClass(position, entry["color"])


def list_saves() -> list[str]:
    if not SAVE_DIR.exists():
        return []
    return sorted(f.stem for f in SAVE_DIR.glob("*.json"))


def delete_save(filename: str) -> bool:
    filepath = SAVE_DIR / f"{filename}.json"
    if filepath.exists():
        os.remove(filepath)
        return True
    return False