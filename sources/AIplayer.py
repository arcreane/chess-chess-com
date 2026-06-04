

class AIbot:
    def __init__(self, name = "bot")
        self.name = name

    def dec_coups(self , board):
        coups = list(board.legal_moves)
        return ramdom.choice(coups)