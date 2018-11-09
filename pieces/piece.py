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

    @staticmethod
    def sign(n):
        if n > 0:
            return 1
        elif n < 0:
            return -1
        else:
            return 0

    def getMoves(self):
        """Return set of valid moves using absolute coordinates"""
        rank, _file = self.position
        if self.LEGALMOVES is None:
            return moves.AnyMove()
        absoluteMoves = set()
        for relativePos in self.LEGALMOVES:
            absolutePos = (relativePos[0] + rank, relativePos[1] + _file)
            for a in absolutePos:
                if a >= 8 or a <= -1:
                    break
            else:
                # Loop was finished, both indices in [0,7]
                absoluteMoves.add(absolutePos)

        return absoluteMoves

    def executeMove(self, board, lastPos, consequences):
        # Optionally implemented by pieces to alter their internal
        # state after a given move is executed
        pass

