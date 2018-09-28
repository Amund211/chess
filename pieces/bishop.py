#! /usr/bin/env python

from . import moves
from .piece import Piece

class Bishop(Piece):
    LEGALMOVES = moves.bishopMoves()

    def move(self, board, current, target):
        """Return True if move is valid in an isolated sense"""
        if target not in self.getMoves(current):
            False, None
        relative = (target[0] - current[0], target[1] - current[1])
        scanRank, scanFile = current

        dirRank = self.sign(relative[0])
        dirFile = self.sign(relative[1])

        # Start scanning one square over
        scanPos = (scanRank + dirRank, scanFile + dirFile)
        while scanPos != target:
            square = board[scanPos]
            if square is not None:
                # Piece blocking path to target
                return False, None
            scanRank += dirRank
            scanFile += dirFile
            scanPos = (scanRank, scanFile)

        # All squares free up until target
        square = board[target]
        if square is None:
            # Vacant square, can move
            return True, None
        elif square.color is not self.color:
            # Enemy square, can capture
            return True, None
        else:
            return False, None

    @staticmethod
    def sign(n):
        if n > 0:
            return 1
        elif n < 0:
            return -1
        else:
            return 0

