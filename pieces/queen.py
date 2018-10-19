#! /usr/bin/env python3

from . import moves, WHITE, BLACK
from .piece import Piece

class Queen(Piece):
    LEGALMOVES = moves.queenMoves()

    def __str__(self):
        if self.color == WHITE:
            return "\N{WHITE CHESS QUEEN}"
        else:
            return "\N{BLACK CHESS QUEEN}"

    def validateMove(self, board, target):
        """Return True if move is valid in an isolated sense"""
        if target not in self.getMoves(self.position):
            False, None
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
                return False, None
            scanRank += dirRank
            scanFile += dirFile
            scanPos = (scanRank, scanFile)

        # All squares free up until target
        square = board[target]
        if square is None:
            # Vacant square, can move
            return True, None
        elif square.color != self.color:
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
