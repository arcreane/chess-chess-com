from abc import ABC, abstractmethod


class Piece (ABC):
    """
    Classe abstraite commune à toutes les pièces.
    Chaque pièce possède au minimum :
    - une position
    - une couleur (0 = blanc, 1 = noir)
    """

    def __init__(self, position, color):
        self.position = position
        self.color = color

    def move_to(self, new_position):

        self.position = new_position
#mettre a jour la position de la pièce

    def is_same_color(self, other_piece):

        return other_piece is not None and self.color == other_piece.color
#Verifier que on ne mange pas une pièce de la meme couleur

    @abstractmethod
    def isValidMove(self, newPosition, board):

        pass
#Verifier si le deplacement est possible
    @abstractmethod
    def __str__(self):

        pass
#Donne l'ID de la pièce