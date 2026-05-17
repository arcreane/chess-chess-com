import sys
from src.chess_game import Chess
from src.save import load_game, list_saves


def main() -> None:
    args = sys.argv[1:]
    vs_ai = "--ai" in args

    chess = Chess(vs_ai=vs_ai)


    if "--load" in args:
        try:
            idx = args.index("--load")
            filename = args[idx + 1]
            load_game(chess, filename)
            print(f"Partie chargée depuis 'saves/{filename}.json'")
        except (IndexError, FileNotFoundError) as e:
            print(f"Impossible de charger : {e}")
            print(f"  Sauvegardes disponibles : {list_saves() or '(aucune)'}")
            return

    chess.play()


if __name__ == "__main__":
    main()