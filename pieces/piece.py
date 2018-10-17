#! /usr/bin/env python3

from . import moves, WHITE, BLACK

class Piece():
    def __init_subclass__(cls):
        if not callable(getattr(cls, "validateMove", None)):
            raise NotImplementedError("Piece class '{}' has no method 'validateMove'".format(cls.__name__))
        if getattr(cls, "LEGALMOVES", None) is None:
            raise NotImplementedError("Piece class '{}' has no property LEGALMOVES".format(cls.__name__))

    def __init__(self, color=WHITE, position=None):
        if color is not WHITE and color is not BLACK:
            raise ValueError("Invalid color for {}: '{}'".format(type(self).__name__, color))
        self.color = color
        self.position = position

    def __repr__(self):
        return (self.__class__.__qualname__ +
                f"(color={self.color!r}, position={self.position!r})")

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

    def executeMove(self, board, target, consequences):
        # Optionally implemented by pieces to alter their internal
        # state after a given move is executed
        pass

