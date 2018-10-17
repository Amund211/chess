#! /usr/bin/env python3

from . import moves, WHITE, BLACK
from .piece import Piece
from .rook import Rook

class King(Piece):
    LEGALMOVES = moves.kingMoves()

    def __init__(self, *args, hasMoved=False, **kwargs):
        self.hasMoved = hasMoved
        super().__init__(*args, **kwargs)

    def validateMove(self, board, current, target):
        """Return True if move is valid in an isolated sense"""
        if target not in self.getMoves(current):
            return False, None

        if abs(current[1] - target[1]) != 2:
            # Regular move
            piece = board[target]
            if piece is None:
                return True, None
            elif piece.color != self.color:
                return True, None
        else:
            # Castling move
            if current[0] != (0 if self.color is WHITE else 7):
                # Can't castle unless on your side's first rank
                return False, None
            if self.hasMoved:
                return False, None

            # Cannot castle from check
            # b.checkTest(current)

            # Searching for rook to castle with using a
            # hard coded position, only works in default game
            if target[1] > current[1]:
                # Kingside castle (short)
                dirFile = 1
            else:
                # Queenside castle (long)
                dirFile = -1

            scanFile = current[1] + dirFile
            castleCheck = False
            rookFile = None
            while scanFile >= 0 and scanFile < 8:
                # Cannot castle through check
                # b.checkTest((current[0], scanFile))

                # Scan for rook or empty space
                square = board[(current[0], scanFile)]
                if square is None:
                    # Empty -> search next square
                    scanFile += dirFile
                else:
                    if type(square) is Rook:
                        if square.color is self.color and not square.hasMoved:
                            # Rook and path valid to castle
                            rookFile = scanFile
                            break
                    else:
                        # Met non-rook -> invalid move
                        return False, None
            else:
                # Found no rook
                return False, None

            # Found rook and clear path
            return True, [(current[0], rookFile), (current[0], current[1] + dirFile)]

