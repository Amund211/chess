#! /usr/bin/env python

"""
Pieces are defined as a class with the following properties:

Methods:
    move: take an input of a boardstate and a current and target position
          return True is move is valid in an isolated sense

Properties:
    color: The color of the piece

Properties unique to spesific pieces should be documented
in the piece's docstring
"""

__all__ = ["WHITE", "BLACK", "CAPTURE", "DOUBLE", "MOVE", "PROMOTE", "RELOCATE", "Piece", "King", "Queen", "Bishop", "Knight", "Rook", "Pawn"]

# Color comparisins can be done using is, because python caches
# small integers, and thus they refer to the same object in memory
#
# >>> a, b = 1, 1
# >>> a is b
# True

WHITE = 1
BLACK = -1


# Consequences

# Flag for capturing an opposing piece
# Data: position of target piece
CAPTURE = "captureflag"

# Flag for setting a pawns passant attribute
# Data: position of pawn (before move)
DOUBLE = "doubleflag"

# Flag for setting hasMoved property on a piece
# Data: position of piece
MOVE = "moveflag"

# Flag for pawn promotion
# Data: type of promotion
PROMOTE = "promoteflag"

# Flag for moving a piece
# Data: tuple of (currPos, targetPos)
RELOCATE = "relocateflag"


from .piece import Piece
from .king import King
from .queen import Queen
from .bishop import Bishop
from .knight import Knight
from .rook import Rook
from .pawn import Pawn

