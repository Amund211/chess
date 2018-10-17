#! /usr/bin/env python3

from . import moves, WHITE, BLACK
from .piece import Piece
from .rook import Rook

class King(Piece):
    LEGALMOVES = moves.kingMoves()

    def __init__(self, *args, hasMoved=False, **kwargs):
        self.hasMoved = hasMoved
        super().__init__(*args, **kwargs)

    def __repr__(self):
        base = super().__repr__()[:-1]
        return (base +
                f", hasMoved={self.hasMoved!r})")

    def validateMove(self, board, target):
        """Return True if move is valid in an isolated sense"""
        if target not in self.getMoves(self.position):
            return False, None

        if abs(self.position[1] - target[1]) != 2:
            # Regular move
            piece = board[target]
            if piece is None:
                return True, None
            elif piece.color != self.color:
                return True, None
        else:
            # Castling move
            if self.position[0] != (0 if self.color == WHITE else 7):
                # Can't castle unless on your side's first rank
                return False, None
            if self.hasMoved:
                return False, None

            # Cannot castle from check
            # b.checkTest(self.position)

            # Searching for rook to castle with using a
            # hard coded position, only works in default game
            if target[1] > self.position[1]:
                # Kingside castle (short)
                dirFile = 1
            else:
                # Queenside castle (long)
                dirFile = -1

            scanFile = self.position[1] + dirFile
            castleCheck = False
            rookFile = None
            while scanFile >= 0 and scanFile < 8:
                # Cannot castle through check
                # b.checkTest((self.position[0], scanFile))

                # Scan for rook or empty space
                square = board[(self.position[0], scanFile)]
                if square is None:
                    # Empty -> search next square
                    scanFile += dirFile
                else:
                    if type(square) is Rook:
                        if square.color == self.color and not square.hasMoved:
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
            return True, [(self.position[0], rookFile), (self.position[0], self.position[1] + dirFile)]

    def executeMove(self, board, target, consequences):
        self.hasMoved = True

        # Castle
        if len(consequences) != 0:
            rookPos = consequences[0][1]
            board[rookPos].hasMoved = True

