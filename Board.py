#! /usr/bin/env python

import copy
from .pieces import Piece
from .utilities import *
from .states import STATES

__all__ = ["Board"]

class Board():
    def __init__(self, gamestate=STATES["default"], moves=None):
        """
        Initialize the board

        If given no inputs, sets up a default starting board.
        If a gamestate is given (tuple (boardstate, toMove) then this state
        is written to the board. If a list of moves are given (AN) then these
        are attempted executed.  When both a gamestate and list of moves are given,
        the state is written, and the moves are then attempted executed.


        Properties:

        boardstate: 2-dim list of the positions on the board. The first dimension
            contains the ranks (1-8), while the second contains the files (A-H).
            This enables switching perspective (White/Black) by simply reversing
            the outer list.

            The values for rank and file are both mapped to numbers 0-7.
            (A4 then maps to 3,0)

        toMove: indicates whether WHITE or BLACK is to move
        """

        # Populate board
        stateValidity = self.validateState(gamestate)
        if not stateValidity[0]:
            # Invalid gamestate with reason stateValidity[1]
            raise StateError(stateValidity[1])

        self._populate(gamestate)

    def _populate(self, gamestate):
        """Sets internal gamestate to given state"""
        # Make deep copy of selected boardstate to avoid interference
        self.boardstate = copy.deepcopy(gamestate[0])
        self.toMove = gamestate[1]

    def __getitem__(self, key):
        """
        Called to implement the evaluation of self[key]

        When key is a position tuple, (0-7, 0-7) the value
        at that position in the boardstate is returned.

        If the key is not a tuple, or the values are outside
        of the valid range, IndexError is raised. This is
        done by the 'validateKey' method.
        """
        # Validate key
        keyValidity = self.validateKey(key)
        if not keyValidity[0]:
            # Invalid key with reason keyValidity[1]
            raise IndexError(keyValidity[1])

        return self.boardstate[key[0]][key[1]]

    def __setitem__(self, key, value):
        """
        Called to implement assignment to self[key]

        When key is a position tuple, (0-7, 0-7) the given
        value is written to that position.

        If the key is not a tuple, or the values are outside
        of the valid range, IndexError is raised. This is
        done by the 'validateKey' method.

        If the given value is neither None or an instance
        of Piece, TypeError is raised.
        """
        # Validate key
        keyValidity = self.validateKey(key)
        if not keyValidity[0]:
            # Invalid key with reason keyValidity[1]
            raise IndexError(keyValidity[1])

        # Validate new value
        if value is not None and not isinstance(value, Piece):
            raise TypeError("Given value must be either None, or an instance of Piece")

        self.boardstate[key[0]][key[1]] = value


    @staticmethod
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


    @staticmethod
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

