#! /usr/bin/env python

from Pieces import *

__all__ = ["STATES"]

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

STATES["default"] = (default, WHITE)
STATES["empty"] = (empty, WHITE)
