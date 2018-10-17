#! /usr/bin/env python3

from . import moves, WHITE, BLACK
from .piece import Piece

class Pawn(Piece):
    LEGALMOVES = moves.pawnMoves()

    def __init__(self, *args, hasMoved=False, passant=False, **kwargs):
        self.hasMoved = hasMoved
        self.passant = passant
        super().__init__(*args, **kwargs)
        # White pawns can only move upwards in rank
        self.direction = 1 if self.color is WHITE else -1

    def validateMove(self, board, current, target):
        """Return True if move is valid in an isolated sense"""
        if target not in self.getMoves(current):
            return False, None
        if current[1] != target[1]:
            # Pawn has changed files -> capture
            if board[target] is not None:
                if board[target].color is self.color:
                    # Can't capture own piece
                    return False, None
                else:
                    # Capture
                    return True, None
            # En passant
            passantTarget = (target[0], target[1] - self.direction)
            passantPiece = board[passantTarget]
            if type(passantPiece) == Pawn:
                if passantPiece.passant and passantPiece.color is not self.color:
                    return True, [passantTarget, None]
            # No passant
            return False, None
        else:
            # Pawn has stayed in file -> move
            relative = (target[0] - current[0], target[1] - current[1])
            if relative[0] == 2 * self.direction:
                # Must be first move
                if self.hasMoved:
                    return False, None

                # Two sqares ahead empty
                if board[(target[0] + self.direction, target[1])] is not None:
                    return False, None
                if board[(target[0] + 2 * self.direction, target[1])] is not None:
                    return False, None

                return True, None
            elif relative[0] == self.direction:
                if board[(target[0] + self.direction, target[1])] is not None:
                    return False, None
                # Sqare ahead empty
                return True, None
            else:
                raise ValueError("Move somehow invalid. current, target:", current, target)

