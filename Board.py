#! /usr/bin/env python

import copy
from states import STATES

__all__ = ["Board"]

class Board():
    def __init__(self, state=None, moves=None):
        """
        Initialize the board

        If given no inputs, sets up a default starting board.
        If a state is given (type: Board) then this state is written to the board.
        If a list of moves are given (AN) then these are attempted executed.
        When both a state and list of moves are given, the state is written,
        and the moves are then attempted executed.

        Properties:

        state: 2-dim list of the positions on the board. The first dimension
            contains the ranks (1-8), while the second contains the files (A-H).
            This enables switching perspective (White/Black) by simply reversing
            the first list.

            The values for rank and file are both mapped to numbers 0-7.
            (A4 then maps to 3,0)

        toMove: indicates whether WHITE or BLACK is to move
        """

        # Populate board
        if state is None:
            # No given state -> default starting board
            self.populate("default")
        else:
            validity = self.validateState(state)
            if validity[0]:
                self.populate(state)
            else:
                # Invalid state with reason validity[1]
                raise StateError(validity[1])

    def populate(self, state=None, preset="default"):
        """Sets internal state to given state or preset"""
        # Finding new state
        if state is not None:
            newState = state
        elif preset in STATES:
            newState = STATES[preset]
        else:
            # No given state and invalid preset
            raise ValueError("The given preset \"{}\" is not defined or could not be found.\nList of defined presets:\n{}".format(preset, list(STATES.keys())))

        # Make deep copy of selected state to avoid interference
        self.state = copy.deepcopy(newState)

    def validateState(self, state):
        """
        Validates a state by testing for size of board, type of pieces and game logic.
        
        The first returned element is True for valid states, and False otherwise
        The second returned element is the given reason for not passing validation
        """
        if len(state) != 8:
            # A state must have exactly 8 ranks
            return False, "State has {} ranks, should be 8".format(len(state))

        for rankIndex, rank in enumerate(state):
            if len(rank) != 8:
                # Each rank must have exactly 8 files
                return False, "Rank {} has {} files, should be 8".format(rankIndex, len(rank))
            
            for fileIndex, square in enumerate(rank):
                if square is not None and type(square) not in Pieces:
                    # Each square must be either empty, or contain
                    # a valid piece
                    return False, "Value in position ({}, {}) was not recognized as a piece".format(rankIndex, fileIndex)

        # Verify validity under game logic (checks, pawns etc.)
        return True

