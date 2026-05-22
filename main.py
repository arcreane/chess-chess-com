import sys
from src.chess_game import Chess
from src.sauvegarde2 import save_game, load_game

def main():
    args = sys.argv[1:]
    
    jeu = Chess(vs_ai="--ai" in args)

    if "--load" in args:
        index = args.index("--load")
        nom_fich = args[index + 1]
        load_game(jeu, nom_fich)
    
    jeu.play()

if __name__ == "__main__":
    main()
