#! /usr/bin/env python

from . import moves, WHITE, BLACK
from .piece import Piece

class Rook(Piece):
    LEGALMOVES = moves.rookMoves()

    def move(self, board, current, target):
        """Return True if move is valid in an isolated sense"""
        return True

