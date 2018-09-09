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

__all__ = ["WHITE", "BLACK", "King", "Queen", "Bishop", "Knight", "Rook",  "Pawn", "Pieces"]

# Color comparisins can be done using is, because python caches
# small integers, and thus they refer to the same object in memory
#
# >>> 1 is 1
# True
WHITE = 0
BLACK = 1


class King():
    def __init__(self, color=WHITE, hasMoved=False):
        self.color = color
        self.hasMoved = hasMoved

    def move(self, board, current, target):
        """Returns True if move is valid in an isolated sense"""
        return True


class Queen():
    def __init__(self, color=WHITE, hasMoved=False):
        self.color = color
        self.hasMoved = hasMoved

    def move(self, board, current, target):
        """Returns True if move is valid in an isolated sense"""
        return True


class Bishop():
    def __init__(self, color=WHITE, hasMoved=False):
        self.color = color
        self.hasMoved = hasMoved

    def move(self, board, current, target):
        """Returns True if move is valid in an isolated sense"""
        return True


class Knight():
    def __init__(self, color=WHITE, hasMoved=False):
        self.color = color
        self.hasMoved = hasMoved

    def move(self, board, current, target):
        """Returns True if move is valid in an isolated sense"""
        return True


class Rook():
    def __init__(self, color=WHITE, hasMoved=False):
        self.color = color
        self.hasMoved = hasMoved

    def move(self, board, current, target):
        """Returns True if move is valid in an isolated sense"""
        return True


class Pawn():
    def __init__(self, color=WHITE, hasMoved=False):
        self.color = color
        self.hasMoved = hasMoved

    def move(self, board, current, target):
        """Returns True if move is valid in an isolated sense"""
        return True


Pieces = set([King, Queen, Bishop, Knight, Rook, Pawn])
