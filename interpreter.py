#! /usr/bin/env python3

import re

from .Board import KING, LIVING
from .utilities import *
from .pieces import *
from .position import toHuman, toInternal


files = "a-h"
ranks = "1-8"
pieces = "KRBNQ"

# Needs check for piece is pawn when promotion
mvExp = f"^(?:(?P<piece>[{pieces}]?)" \
        f"(?P<depFile>[{files}])?" \
        f"(?P<depRank>[{ranks}])?" \
        f"(?P<capture>[x])?" \
        f"(?P<arrFile>[{files}])" \
        f"(?P<arrRank>[{ranks}])" \
        f"(?:=(?P<promotion>[{pieces}]))?" \
        f"|" \
        f"(?P<castle>O-O(?:-O)?))" \
        f"(?:[#+]?)$"

mvReg = re.compile(mvExp)

NAMES = {
        "K": King,
        "Q": Queen,
        "R": Rook,
        "B": Bishop,
        "N": Knight,
        "": Pawn
}


def toInternal(huRank=None, huFile=None):
    if huRank is None:
        if huFile is None:
            return None, None
        return None, ord(huFile) - 97
    elif huFile is None:
        return int(huRank) - 1, None
    else:
        # Neither None
        return int(huRank) - 1, ord(huFile) - 97


def toHuman(inRank=None, inFile=None):
    if inRank is None:
        return chr(inFile + 97)
    elif inFile is None:
        return str(inRank + 1)
    else:
        # Neither None
        return str(inRank + 1), chr(inFile + 97)


def interpretMove(board, mvStr):
    """
    Interpret move given in algebraic notation
    to internal (current, target) representation.
    """
    match = re.match(mvReg, mvStr)
    if match is None:
        raise MoveError(mvStr, "Invalid syntax!")

    # Check for castle
    castle = match.group("castle")

    if castle is not None:
        kingPos = board.pieces[board.toMove][KING].position
        if castle == "O-O-O":
            # Long castle, negative files
            return kingPos, (kingPos[0], kingPos[1] - 2), None
        else:
            return kingPos, (kingPos[0], kingPos[1] + 2), None

    depFile = match.group("depFile")
    depRank = match.group("depRank")

    arrFile = match.group("arrFile")
    arrRank = match.group("arrRank")

    pieceType = NAMES[match.group("piece")]
    capture = match.group("capture") is not None

    promotion = match.group("promotion")

    # Get internal representation for positions
    currRank, currFile = toInternal(depRank, depFile)
    target = toInternal(arrRank, arrFile)


    candidates = board.pieces[board.toMove][LIVING]
    result = []

    # Copy of list to avoid interference
    for candidate in candidates[:]:
        if type(candidate) is not pieceType:
            continue
        if currRank is not None:
            # Current rank of piece specified
            if candidate.position[0] != currRank:
                continue
        if currFile is not None:
            # Current rank of piece specified
            if candidate.position[1] != currFile:
                continue

        if board.move(candidate.position, target, promotion=promotion, validate=True):
            result.append(candidate)

    if len(result) == 0:
        raise MoveError(mvStr, "No piece can make that move!")
    elif len(result) > 1:
        raise MoveError(mvStr, "Ambigous move! Disambiguate by giving a departing rank or file.")


    return result[0].position, target, promotion


