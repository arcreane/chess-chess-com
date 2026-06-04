import sys


def main():
    args = sys.argv[1:]

    # Interface graphique (necessite pygame : pip install pygame)
    if "--gui" in args:
        from sources.graphism import mainloop
        mainloop.demo()
        return

    # Mode texte
    from sources.chess_game import Chess
    from sources.sauvegarde2 import save_game, load_game

    jeu = Chess(vs_ai="--ai" in args)
    if "--load" in args:
        index = args.index("--load")
        nom_fich = args[index + 1]
        load_game(jeu, nom_fich)

    jeu.play()


if __name__ == "__main__":
    main()
