#! /usr/bin/env python

__all__ = ["AnyMove", "kingMoves", "queenMoves", "bishopMoves", "knightMoves", "rookMoves", "pawnMoves"]

from ..utilities import validateKey


class AnyMove():
    """
    Represents a set containing all squares on the board

    This is achived by returning True on membership-tests
    for any valid position tuple
    Iteration of this object returns a all squares on
    the board.
    """
    def __init__(self):
        self.rank = 0
        self._file = 0

    def __contains__(self, item):
        keyValidity = validateKey(item)
        return keyValidity[0]

    def __iter__(self):
        return self

    def __next__(self):
        if self._file < 8:
            item = (self.rank, self._file)
            self.rank += 1
            if self.rank == 8:
                self.rank -= 8
                self._file += 1
            return item
        else:
            self.rank = 0
            self._file = 0
            raise StopIteration()


def kingMoves():
    allMoves = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == j == 0:
                continue
            allMoves.append((i, j))
    return allMoves


def queenMoves():
    allMoves = []
    for i in range(-7, 8):
        if i == 0:
            continue
        allMoves.append((0, i))
        allMoves.append((i, 0))
        allMoves.append((i, i))
        allMoves.append((-i, i))
    return allMoves


def bishopMoves():
    allMoves = []
    for i in range(-7, 8):
        if i == 0:
            continue
        allMoves.append((i, i))
        allMoves.append((-i, i))
    return allMoves


def knightMoves():
    allMoves = []
    for i in range(4):
        highSign = -1 if (i & 2 == 2) else 1
        lowSign = -1 if (i & 1 == 1) else 1
        allMoves.append((2 * highSign, 1 * lowSign))
        allMoves.append((1 * highSign, 2 * lowSign))
    return allMoves


def rookMoves():
    allMoves = []
    for i in range(-7, 8):
        if i == 0:
            continue
        allMoves.append((0, i))
        allMoves.append((i, 0))
    return allMoves


def pawnMoves():
    return [(1, 0), (2, 0), (1, 1), (1, -1)]

