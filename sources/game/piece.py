from abc import ABC, abstractmethod


class Piece (ABC):

    def __init__(self, position, color):
        self.position = position
        self.color = color
        self.has_moved = False
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

from king import King
from queen import Queen
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
from Pawn import Pawn