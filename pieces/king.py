#! /usr/bin/env python

from . import moves, WHITE, BLACK
from .piece import Piece

class King(Piece):
    LEGALMOVES = moves.kingMoves()

    def __init__(self, *args, hasMoved=False, **kwargs):
        self.hasMoved = hasMoved
        super().__init__(*args, **kwargs)

    def move(self, board, current, target):
        """Return True if move is valid in an isolated sense"""
        if target in self.getMoves(current):
            piece = board[target]
            if piece is None:
                return True
            elif piece.color != self.color:
                return True
        return False

