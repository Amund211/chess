#! /usr/bin/env python

import copy
from Pieces import *
from utilities import *
from states import STATES

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
        stateValidity = validateState(gamestate)
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
        keyValidity = validateKey(key)
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
        keyValidity = validateKey(key)
        if not keyValidity[0]:
            # Invalid key with reason keyValidity[1]
            raise IndexError(keyValidity[1])

        # Validate new value
        if value is not None and not isinstance(value, Piece):
            raise TypeError("Given value must be either None, or an instance of Piece")

        self.boardstate[key[0]][key[1]] = value

