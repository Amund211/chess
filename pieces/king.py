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

    def __str__(self):
        if self.color == WHITE:
            return "\N{WHITE CHESS KING}"
        else:
            return "\N{BLACK CHESS KING}"

    def validateMove(self, board, target):
        """Return True if move is valid in an isolated sense"""
        if target not in self.getMoves():
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

            _file = self.position[1]
            offset = dirFile
            castleCheck = False
            rookFile = None
            while _file + offset >= 0 and _file + offset < 8:
                # Cannot castle through check
                # b.checkTest((self.position[0], scanFile))

                # Scan for rook or empty space
                square = board[(self.position[0], _file + offset)]
                if square is None:
                    # Empty -> search next square
                    offset += dirFile
                else:
                    if type(square) is Rook:
                        if square.color == self.color and not square.hasMoved and abs(offset) >= 3:
                            # Rook valid to castle and clear path
                            rookFile = _file + offset
                            break
                        else:
                            # Met rook unable to castle
                            return False, None
                    else:
                        # Met non-rook -> invalid move
                        return False, None
            else:
                # Found no rook
                return False, None

            # Found rook and clear path
            return True, [(self.position[0], rookFile), (self.position[0], self.position[1] + dirFile)]

    def executeMove(self, board, lastPos, consequences):
        self.hasMoved = True

        # Castle
        if consequences is not None:
            rookPos = consequences[1]
            board[rookPos].hasMoved = True

