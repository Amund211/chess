#! /usr/bin/env python

__all__ = ["validateKey", "validateState", "NotationError", "MoveError", "StateError"]


def validateKey(key):
    if type(key) is not tuple:
        # Preferably raise TypeError
        return False, "Index for instance of Board must be a position tuple."
    elif len(key) != 2:
        return False, "Key must be a tuple of length 2"
    elif key[0] < 0 or key[0] > 7:
        return False, "Position values must be in the range 0-7"
    elif key[1] < 0 or key[1] > 7:
        return False, "Position values must be in the range 0-7"

    # Key valid
    return True, "Passed validation"


def validateState(gamestate):
    """
    Validates a gamestate by testing for size of board, type of pieces and game logic.
    
    The first returned element is True for valid gamestates, and False otherwise
    The second returned element is the given reason for not passing validation
    """
    boardstate = gamestate[0]

    if len(boardstate) != 8:
        # A state must have exactly 8 ranks
        return False, "State has {} ranks, should be 8".format(len(boardstate))

    for rankIndex, rank in enumerate(boardstate):
        if len(rank) != 8:
            # Each rank must have exactly 8 files
            return False, "Rank {} has {} files, should be 8".format(rankIndex, len(rank))
        
        for fileIndex, square in enumerate(rank):
            if square is not None and not isinstance(square, Piece):
                # Each square must be either empty, or contain
                # a valid piece
                return False, "Value in position ({}, {}) was not recognized as an empty square or a piece".format(rankIndex, fileIndex)

    # Verify validity under game logic (checks, pawns etc.)
    return True, "Passed validation"


class ChessError(Exception):
    """Base class for exceptions in the chess engine"""
    def __init_subclass__(cls):
        if not callable(getattr(cls, "response", None)):
            raise NotImplementedError("Child of ChessError has no method response")

    def __init__(self, expression, reason=None):
        # Save properties to instance
        self.expression = expression
        self.reason = reason

    def __str__(self):
        # Refer to child's implementation of method 'response'
        return self.response()


class NotationError(ChessError):
    """Exception raised for erroneous notation"""
    def response(self):
        response = "\"{}\" is invalid algebraic notation.".format(self.expression)
        return response + ("" if self.reason is None else " ({})".format(self.reason))


class MoveError(ChessError):
    """Exception raised for invalid moves"""
    def response(self):
        response = "\"{}\" is an invalid move.".format(self.expression)
        return response + ("" if self.reason is None else " ({})".format(self.reason))


class StateError(ChessError):
    """Exception raised for invalid states"""
    def response(self):
        response = "The given state is invalid:\n\n{}\n".format(self.expression)
        return response + ("" if self.reason is None else "({})".format(self.reason))



