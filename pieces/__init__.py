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

__all__ = ["WHITE", "BLACK", "Piece", "King", "Queen", "Bishop", "Knight", "Rook", "Pawn"]

WHITE = 0
BLACK = 1

from .piece import Piece
from .king import King
from .queen import Queen
from .bishop import Bishop
from .knight import Knight
from .rook import Rook
from .pawn import Pawn

