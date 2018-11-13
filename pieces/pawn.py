#! /usr/bin/env python3

from . import moves, WHITE, BLACK, King, Queen, Rook, Bishop, Knight
from .flags import CAPTURE, DOUBLE, PROMOTE
from .piece import Piece

SYMBOLS = {
        "Q": Queen,
        "R": Rook,
        "B": Bishop,
        "N": Knight
}


class Pawn(Piece):
    def __init__(self, *args, hasMoved=False, passant=False, **kwargs):
        self.hasMoved = hasMoved
        self.passant = passant
        super().__init__(*args, **kwargs)
        # White pawns can only move upwards in rank
        self.direction = self.color
        self.LEGALMOVES = moves.pawnMoves(self.direction)

    def __repr__(self):
        base = super().__repr__()[:-1]
        return (base +
                f", hasMoved={self.hasMoved!r}"
                f", passant={self.passant!r})")

    def __str__(self):
        if self.color is WHITE:
            return "\N{WHITE CHESS PAWN}"
        else:
            return "\N{BLACK CHESS PAWN}"

    def validateMove(self, board, target, promotion=None):
        """Return True if move is valid in an isolated sense"""
        if target not in self.getMoves():
            return False, {}

        if self.position[1] != target[1]:
            # Pawn has changed files -> capture
            if board[target] is not None:
                # Piece in target position -> regular capture
                if board[target].color is self.color:
                    # Can't capture own piece
                    return False, {}
                else:
                    # Capture
                    if target[0] == (-self.color - 1) % 9:
                        # Target rank is 0 or 7, depending on color
                        if promotion not in SYMBOLS:
                            # Invalid symbol to promote to
                            return False, {}
                        return True, {CAPTURE: target, PROMOTE: (self.position, SYMBOLS[promotion](color=self.color))}
                    return True, {CAPTURE: target}
            else:
                # En passant
                passantTarget = (target[0] - self.direction, target[1])
                passantPiece = board[passantTarget]
                if type(passantPiece) is Pawn:
                    if passantPiece.passant and passantPiece.color is not self.color:
                        return True, {CAPTURE: passantTarget}
                # No passant
                return False, {}
        else:
            # Pawn has stayed in file -> move
            relative = (target[0] - self.position[0], target[1] - self.position[1])
            if relative[0] == 2 * self.direction:
                # Must be first move
                if self.hasMoved:
                    return False, {}

                # Two squares ahead empty
                if board[(self.position[0] + self.direction, target[1])] is not None:
                    return False, {}
                if board[target] is not None:
                    return False, {}
                return True, {DOUBLE: (self.position, target)}
            elif relative[0] == self.direction:
                # Sqare ahead occupied
                if board[target] is not None:
                    return False, {}

                if target[0] == (-self.color - 1) % 9:
                    # Target rank is 0 or 7, depending on color
                    if promotion not in SYMBOLS:
                        # Invalid symbol to promote to
                        return False, {}
                    return True, {PROMOTE: (self.position, SYMBOLS[promotion](color=self.color))}

                return True, {}
            else:
                raise ValueError("Move somehow invalid. self.position, target:", self.position, target)

