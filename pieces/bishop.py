#! /usr/bin/env python3

from . import moves, WHITE, BLACK
from .flags import CAPTURE
from .piece import Piece

class Bishop(Piece):
    LEGALMOVES = moves.bishopMoves()

    def __str__(self):
        if self.color is WHITE:
            return "\N{WHITE CHESS BISHOP}"
        else:
            return "\N{BLACK CHESS BISHOP}"


    def validateMove(self, board, target):
        """Return True if move is valid in an isolated sense"""
        if target not in self.getMoves():
            return False, None

        relative = (target[0] - self.position[0], target[1] - self.position[1])
        scanRank, scanFile = self.position

        dirRank = self.sign(relative[0])
        dirFile = self.sign(relative[1])

        # Start scanning one square over
        scanPos = (scanRank + dirRank, scanFile + dirFile)
        while scanPos != target:
            square = board[scanPos]
            if square is not None:
                # Piece blocking path to target
                return False, {}
            scanRank += dirRank
            scanFile += dirFile
            scanPos = (scanRank, scanFile)

        # All squares free up until target
        square = board[target]
        if square is None:
            # Vacant square, can move
            return True, {}
        elif square.color is not self.color:
            # Enemy square, can capture
            return True, {CAPTURE: target}
        else:
            return False, {}

