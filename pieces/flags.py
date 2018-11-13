#! /usr/bin/env python3

from collections import namedtuple
from ..Board import LIVING, GRAVEYARD

__all__ = ["CAPTURE", "DOUBLE", "MOVE", "PROMOTE", "RELOCATE"]

"""
Consequenses as flags

A flag is a namedtuple with the properties execute and revert.
Each of these are functions that take a board and data element,
and mutate the board. The execute method returns data, which is
to be stored and passed to the revert method in case the move needs
to be reverted.
"""


# Datastructure for storing execute and revert functions for the flags
Flag = namedtuple("Flag", ("execute", "revert"))

# Flag for capturing an opposing piece
# Data: position of target piece
def exeCapture(board, data):
    # Semantic meaning of data
    pos = data

    capturedPiece = board[pos]

    # Remove piece from board and living list of opponent
    # add to graveyard of opponent
    board.pieces[-board.toMove][LIVING].remove(capturedPiece)
    board.pieces[-board.toMove][GRAVEYARD].append(capturedPiece)
    board[pos] = None

    return (pos, capturedPiece)


def revCapture(board, revData):
    # Semantic meaning of revData
    pos, capturedPiece = revData

    # Remove piece graveyard of opponent, and add to board and
    # living list
    board.pieces[-board.toMove][LIVING].append(capturedPiece)
    board.pieces[-board.toMove][GRAVEYARD].remove(capturedPiece)
    board[pos] = capturedPiece

CAPTURE = Flag(exeCapture, revCapture)

# Flag for setting a pawns passant attribute
# Data: tuple of pawns positions before and after move
def exeDouble(board, data):
    # Semantic meaning of data
    beforePos, afterPos = data

    # Set passant attribute of piece, and passantPos of board
    board[beforePos].passant = True
    board.passantPos[board.toMove] = afterPos

    return beforePos


def revDouble(board, revData):
    # Semantic meaning of revData
    pos = revData

    # Unset passant attribute of piece, and passantPos of board
    board[pos].passant = False
    board.passantPos[board.toMove] = None


DOUBLE = Flag(exeDouble, revDouble)


# Flag for setting hasMoved property on a piece
# Data: position of piece
def exeMove(board, data):
    # Semantic meaning of data
    pos = data
    # Store current hasMoved value and store in undodict
    status = board[pos].hasMoved

    # Set attribute
    board[pos].hasMoved = True

    return (pos, status)


def revMove(board, revData):
    # Semantic meaning of revData
    pos, status = revData

    # Reset attribute to last value
    board[pos].hasMoved = status


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
    # Semantic meaning of data
    pos1, pos2 = data
    # Alias for pieces involved in swap
    piece1 = board[pos1]
    piece2 = board[pos2]

    # Swap position in board
    board[pos1], board[pos2] = piece2, piece1
    # Set new position on piece(s)
    if piece1 is not None:
        piece1.position = pos2
    if piece2 is not None:
        piece2.position = pos1

    return data


# Swapping pieces is a symmetric operation
revRelocate = exeRelocate

RELOCATE = Flag(exeRelocate, revRelocate)



