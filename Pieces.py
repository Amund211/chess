#! /usr/bin/env python

"""
Pieces are defined as a class with the following properties:

Methods:
    move: take an input of a boardstate and a current and target position
          return True is move is valid in an isolated sense

Properties:
    color: The color of the piece
    hasMoved: Whether the piece has moved this game
"""

__all__ = ["WHITE", "BLACK", "Piece", "King", "Queen", "Bishop", "Knight", "Rook",  "Pawn"]

import moves

# Color comparisins can be done using is, because python caches
# small integers, and thus they refer to the same object in memory
#
# >>> a, b = 1, 1
# >>> a is b
# True
WHITE = 0
BLACK = 1


class Piece():
    def __init_subclass__(cls):
        if not callable(getattr(cls, "move", None)):
            raise NotImplementedError("Piece class '{}' has no method 'move'".format(cls.__name__))
        return
        if getattr(cls, "LEGALMOVES", None) is None:
            raise NotImplementedError("Piece class '{}' has no property LEGALMOVES".format(cls.__name__))

    def __init__(self, color=WHITE):
        if color is not WHITE and color is not BLACK:
            raise ValueError("Invalid color for {}: '{}'".format(type(self).__name__, color))
        self.color = color

    @classmethod
    def getMoves(cls, position):
        """Return set of valid moves using absolute coordinates"""
        rank, _file = position
        if cls.LEGALMOVES is None:
            return moves.AnyMove()
        absoluteMoves = set()
        for relativePos in cls.LEGALMOVES:
            absoluteMoves.add((relativePos[0] + rank, relativePos[1] + _file))

        return absoluteMoves


class King(Piece):
    LEGALMOVES = moves.kingMoves()

    def __init__(self, *args, hasMoved=False, **kwargs):
        self.hasMoved = hasMoved
        super().__init__(*args, **kwargs)

    def move(self, board, current, target):
        """Return True if move is valid in an isolated sense"""
        if target in self.getMoves(current):
            piece = board[target]
            if piece is None:
                return True
            elif piece.color != self.color:
                return True
        return False


class Queen(Piece):
    LEGALMOVES = moves.queenMoves()

    def move(self, board, current, target):
        """Return True if move is valid in an isolated sense"""
        return True


class Bishop(Piece):
    LEGALMOVES = moves.bishopMoves()

    def move(self, board, current, target):
        """Return True if move is valid in an isolated sense"""
        return True


class Knight(Piece):
    LEGALMOVES = moves.knightMoves()

    def move(self, board, current, target):
        """Return True if move is valid in an isolated sense"""
        if target in self.getMoves(current):
            piece = board[target]
            if piece is None:
                return True
            elif piece.color != self.color:
                return True
        return False


class Rook(Piece):
    LEGALMOVES = moves.rookMoves()

    def move(self, board, current, target):
        """Return True if move is valid in an isolated sense"""
        return True


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

