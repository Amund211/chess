#! /usr/bin/env python

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
        """

        # Initialize empty board
        self.state = [[None] * 8] * 8
        
        # Populate board
        self.populate()

    def populate(self, state=None, preset="default"):
        """Verifies given state or preset, and sets internal state"""
        # Finding new state
        if state is not None:
            newState = state
        elif preset in STATES:
            newState = STATES[preset]
        else:
            # No given state and invalid preset
            raise ValueError("The given preset \"{}\" is not defined or could not be found.\nList of defined presets:\n{}".format(preset, list(STATES.keys())))

        # Verifying the new state
        if self.verifyState(state):
            self.state = newState
        else:
            raise StateError(state, "reason")

    def verifyState(self, state):
        """Returns True if given state is valid"""
        return True

            

