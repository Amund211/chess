#! /usr/bin/env python

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

    def move(self, board, current, target):
        """Return True if move is valid in an isolated sense"""
        if current[1] != target[1]:
            # Pawn has changed files -> capture
            if board[target] is not None:
                if board[target].color is self.color:
                    # Can't capture own piece
                    return False
                else:
                    # Capture
                    return True
            # En passant
            passantTarget = board[(target[0], target[1] - self.direction)]
            if type(passantTarget) == Pawn:
                if passantTarget.passant:
                    return True
            # No passant
            return False
        else:
            # Pawn has stayed in file -> move
            relative = (target[0] - current[0], target[1] - current[1])
            if relative[0] == 2 * self.direction:
                # Must be first move
                if self.hasMoved:
                    return False

                # Two sqares ahead empty
                if board[(target[0] + self.direction, target[1])] is not None:
                    return False
                if board[(target[0] + 2 * self.direction, target[1])] is not None:
                    return False

                return True
            elif relative[0] == self.direction:
                if board[(target[0] + self.direction, target[1])] is not None:
                    return False
                # Sqare ahead empty
                return True
            else:
                raise ValueError("Move somehow invalid. current, target:", current, target)

