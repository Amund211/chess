#! /usr/bin/env python

from .pieces import *

__all__ = ["STATES"]


def assignPos(boardstate):
    """Assigns pieces in a boardstate their respective positions."""
    for r, rank in enumerate(boardstate):
        for f, square in enumerate(rank):
            if square is not None:
                square.position = (r, f)


emptyRank = [None] * 8

STATES = {}

default = [
        [Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE), King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)],
        [Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)],
        emptyRank[:],
        emptyRank[:],
        emptyRank[:],
        emptyRank[:],
        [Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)],
        [Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK), King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)]
]
assignPos(default)

empty = [
        emptyRank[:],
        emptyRank[:],
        emptyRank[:],
        emptyRank[:],
        emptyRank[:],
        emptyRank[:],
        emptyRank[:],
        emptyRank[:]
]
assignPos(empty)

STATES["default"] = (default, WHITE)
STATES["empty"] = (empty, WHITE)

