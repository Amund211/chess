#! /usr/bin/env python3

from . import moves, WHITE, BLACK
from .piece import Piece

class Pawn(Piece):
    LEGALMOVES = moves.pawnMoves(1)

    def __init__(self, *args, hasMoved=False, passant=False, **kwargs):
        self.hasMoved = hasMoved
        self.passant = passant
        super().__init__(*args, **kwargs)
        # White pawns can only move upwards in rank
        self.direction = 1 if self.color == WHITE else -1
        if self.color == BLACK:
            self.LEGALMOVES = moves.pawnMoves(self.direction)


    def __repr__(self):
        base = super().__repr__()[:-1]
        return (base +
                f", hasMoved={self.hasMoved!r}"
                f", passant={self.passant!r})")

    def __str__(self):
        if self.color == WHITE:
            return "\N{WHITE CHESS PAWN}"
        else:
            return "\N{BLACK CHESS PAWN}"

    def validateMove(self, board, target):
        """Return True if move is valid in an isolated sense"""
        if target not in self.getMoves():
            return False, None

        if self.position[1] != target[1]:
            # Pawn has changed files -> capture
            if board[target] is not None:
                if board[target].color == self.color:
                    # Can't capture own piece
                    return False, None
                else:
                    # Capture
                    return True, None
            # En passant
            passantTarget = (target[0] - self.direction, target[1])
            print(passantTarget)
            passantPiece = board[passantTarget]
            if type(passantPiece) == Pawn:
                if passantPiece.passant and passantPiece.color != self.color:
                    return True, [passantTarget, None]
            # No passant
            return False, None
        else:
            # Pawn has stayed in file -> move
            relative = (target[0] - self.position[0], target[1] - self.position[1])
            if relative[0] == 2 * self.direction:
                # Must be first move
                if self.hasMoved:
                    return False, None

                # Two sqares ahead empty
                if board[target] is not None:
                    return False, None
                if board[(self.position[0] + 2 * self.direction, target[1])] is not None:
                    return False, None

                return True, None
            elif relative[0] == self.direction:
                if board[target] is not None:
                    return False, None
                # Sqare ahead empty
                return True, None
            else:
                raise ValueError("Move somehow invalid. self.position, target:", self.position, target)

    def executeMove(self, board, target, consequences):
        self.hasMoved = True
        # Set passant flag when moving 2 spaces, otherwise set to False
        self.passant = abs(self.position[0] - target[0]) == 2

