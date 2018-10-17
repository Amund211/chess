#! /usr/bin/env python3

from . import moves
from .piece import Piece

class Knight(Piece):
    LEGALMOVES = moves.knightMoves()

    def validateMove(self, board, target):
        """Return True if move is valid in an isolated sense"""
        if target in self.getMoves(self.position):
            piece = board[target]
            if piece is None:
                return True, None
            elif piece.color is not self.color:
                return True, None
        return False, None

