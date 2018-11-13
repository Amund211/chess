#! /usr/bin/env python3

from collections import namedtuple

__all__ = ["CAPTURE", "DOUBLE", "MOVE", "PROMOTE", "RELOCATE"]

# Consequences

# Datastructure for storing execute and revert functions for the flags
Flag = namedtuple("Flag", ("execute", "revert"))

# Flag for capturing an opposing piece
# Data: position of target piece
def exeCapture(board, data):
    pass


def revCapture(board, revData):
    pass


CAPTURE = Flag(exeCapture, revCapture)

# Flag for setting a pawns passant attribute
# Data: position of pawn (before move)
def exeDouble(board, data):
    pass


def revDouble(board, revData):
    pass


DOUBLE = Flag(exeDouble, revDouble)


# Flag for setting hasMoved property on a piece
# Data: position of piece
def exeMove(board, data):
    pass


def revMove(board, revData):
    pass


MOVE = Flag(exeMove, revMove)

# Flag for pawn promotion
# Data: type of promotion
def exePromote(board, data):
    pass


def revPromote(board, revData):
    pass


PROMOTE = Flag(exePromote, revPromote)

# Flag for moving a piece
# Data: tuple of (currPos, targetPos)
def exeRelocate(board, data):
    pass


def revRelocate(board, revData):
    pass


RELOCATE = Flag(exeRelocate, revRelocate)



