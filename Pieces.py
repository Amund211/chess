#! /usr/bin/env python

"""
Pieces are defined as a class with the following properties:

Methods:
    move: takes an input of a boardstate and a current and target position
          returns True is move is valid in an isolated sense

Properties:
    color: The color of the piece
    hasMoved: Whether the piece has moved this game
"""

__all__ = ["WHITE", "BLACK", "Piece", "King", "Queen", "Bishop", "Knight", "Rook",  "Pawn"]

# Color comparisins can be done using is, because python caches
# small integers, and thus they refer to the same object in memory
#
# >>> a, b = 1, 1
# >>> a is b
# True
WHITE = 0
BLACK = 1


class Piece():
    def __init_subclass__(cls):
        if not callable(getattr(cls, "move", None)):
            raise NotImplementedError("Piece class '{}' has no method 'move'".format(cls.__name__))

    def __init__(self, color=WHITE):
        if color is not WHITE and color is not BLACK:
            raise ValueError("Invalid color for {}: '{}'".format(type(self).__name__, color))
        self.color = color


class King(Piece):
    def __init__(self, *args, hasMoved=False, **kwargs):
        self.hasMoved = hasMoved
        super().__init__(*args, **kwargs)

    def move(self, board, current, target):
        """Returns True if move is valid in an isolated sense"""
        return True


class Queen(Piece):
    def move(self, board, current, target):
        """Returns True if move is valid in an isolated sense"""
        return True


class Bishop(Piece):
    def move(self, board, current, target):
        """Returns True if move is valid in an isolated sense"""
        return True


class Knight(Piece):
    def move(self, board, current, target):
        """Returns True if move is valid in an isolated sense"""
        return True


class Rook(Piece):
    def move(self, board, current, target):
        """Returns True if move is valid in an isolated sense"""
        return True


class Pawn(Piece):
    def __init__(self, *args, hasMoved=False, **kwargs):
        self.hasMoved = hasMoved
        super().__init__(*args, **kwargs)

    def move(self, board, current, target):
        """Returns True if move is valid in an isolated sense"""
        return True

