#! /usr/bin/env python3

from . import moves, WHITE, BLACK
from .flags import CAPTURE
from .piece import Piece

class Knight(Piece):
    LEGALMOVES = moves.knightMoves()

    def __str__(self):
        if self.color is WHITE:
            return "\N{WHITE CHESS KNIGHT}"
        else:
            return "\N{BLACK CHESS KNIGHT}"

    def validateMove(self, board, target):
        """Return True if move is valid in an isolated sense"""
        if target in self.getMoves():
            piece = board[target]

            if piece is None:
                return True, {}
            elif piece.color is not self.color:
                return True, {CAPTURE: target}
        return False, {}

