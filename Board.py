#! /usr/bin/env python3

import copy
from .position import toHuman, toInternal
from .pieces import *
from .utilities import *
from .states import STATES

__all__ = ["Board"]

# Indicies for the piece tuples
LIVING = "living"
GRAVEYARD = "graveyard"
KING = "king"


class Board():
    """
    Properties:

    boardstate: 2-dim list of the positions on the board. The first dimension
        contains the ranks (1-8), while the second contains the files (A-H).
        This enables switching perspective (White/Black) by simply reversing
        the outer list.

        The values for rank and file are both mapped to numbers 0-7.
        (A4 then maps to 3,0)

    toMove: indicates whether WHITE or BLACK is to move

    pieces: tuple containing a tuple containing the living pieces and the graveyard for white/black
    """

    def __init__(self, gamestate=STATES["default"], moves=None):
        """
        Initialize the board

        If given no inputs, sets up a default starting board.
        If a gamestate is given (tuple (boardstate, toMove)) then this state
        is written to the board. If a list of moves are given (AN) then these
        are attempted executed.  When both a gamestate and list of moves are given,
        the state is written, and the moves are then attempted executed.
        """

        self.boardstate = None
        self.toMove = None
        self.pieces = {
            WHITE: {LIVING: [], GRAVEYARD: [], KING: None},
            BLACK: {LIVING: [], GRAVEYARD: [], KING: None}
        }

        # Populate board with given state
        self._populate(gamestate)

        # Validate board
        stateValidity = self.validateState(gamestate, True)
        if not stateValidity[0]:
            # Invalid gamestate with reason stateValidity[1]
            raise StateError(stateValidity[1])

    def __str__(self):
        return self.draw(WHITE)

    def draw(self, perspective):
        render = " A B C D E F G H\n"
        n = -1
        if perspective == WHITE:
            view = self.boardstate[::-1]
        else:
            view = self.boardstate[:]
        for rank in view:
            n += 1
            if perspective == WHITE:
                render += str(8-n)
            else:
                render += str(n+1)
            for square in rank:
                if square is None:
                    render += " "
                else:
                    render += str(square)
                render += " "
            render = render[:-1] + "\n"
        return render


    def _populate(self, gamestate):
        """Sets internal gamestate to given state"""
        self.boardstate = []
        # Add to living lists
        for r, rank in enumerate(gamestate[0]):
            newRank = []
            for f, square in enumerate(rank):
                # Add piece to boardstate and piece-list
                pieceCopy = eval(repr(square))
                newRank.append(pieceCopy)
                if pieceCopy is not None:
                    self.pieces[square.color][LIVING].append(pieceCopy)

                # Store reference to King piece
                if type(pieceCopy) is King:
                    self.pieces[square.color][KING] = pieceCopy
            self.boardstate.append(newRank)

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
            raise IndexError(keyValidity[1], key)

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
            raise IndexError(keyValidity[1], key)

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
        elif type(key[0]) is not int or type(key[1]) is not int:
            return False, "Position values must be integers"
        elif key[0] < 0 or key[0] > 7:
            return False, "Position values must be in the range 0-7"
        elif key[1] < 0 or key[1] > 7:
            return False, "Position values must be in the range 0-7"


        # Key valid
        return True, "Passed validation"

    @staticmethod
    def findPiece(pieceList, cls):
        """Return all instances of type cls in iterable pieceList"""
        output = []
        for piece in pieceList:
            if type(piece) is cls:
                output.append(piece)
        return output

    def validateState(self, gamestate, fullCheck=False):
        """
        Validate a gamestate by testing for size of board, type of pieces and game logic.

        The first returned element is True for valid gamestates, and False otherwise
        The second returned element is the given reason for not passing validation
        """
        boardstate, toMove = gamestate

        whiteKing = 0
        blackKing = 0
        if len(boardstate) != 8:
            # A state must have exactly 8 ranks
            return False, "State has {} ranks, should be 8".format(len(boardstate))

        for rankIndex, rank in enumerate(boardstate):
            if len(rank) != 8:
                # Each rank must have exactly 8 files
                return False, "Rank {} has {} files, should be 8".format(rankIndex, len(rank))

            for fileIndex, square in enumerate(rank):
                if square is not None:
                    if not isinstance(square, Piece):
                        # Each square must be either empty, or contain
                        # a valid piece
                        return False, "Value in position ({}, {}) was not recognized as an empty square or a piece".format(rankIndex, fileIndex)
                    elif type(square) is King:
                        if square.color == WHITE:
                            whiteKing += 1
                        else:
                            blackKing += 1
        if blackKing != 1:
            return False, "Board must have exactly one black king. (Not {})".format(blackKing)
        elif whiteKing != 1:
            return False, "Board must have exactly one white king. (Not {})".format(whiteKing)

        if self.inCheck(-self.toMove):
            return False, "Player to move can capture king."

        # Verify validity under game logic (checks, pawns etc.)
        return True, "Passed validation"

    def isContested(self, player, position):
        """Return True if given position is contested by the given player."""
        attacking = self.pieces[player][LIVING]

        target = self[position]
        if target is not None:
            if target.color == player:
                return False

        dummy = Piece(-player)
        self[position] = dummy

        for attacker in attacking:
            valid, consequences = attacker.validateMove(self, position)
            if valid:
                break

        # Reset position
        self[position] = target

        return valid

    def inCheck(self, player):
        """Return True if given player is currently in check."""
        kingPos = self.pieces[player][KING].position
        return self.isContested(-player, kingPos)

    def move(self, current, target):
        """Execute given move if valid, otherwise raise MoveError."""
        piece = self[current]
        if piece is None:
            raise MoveError("Square is empty, no piece to move!")
        elif piece.color != self.toMove:
            raise MoveError("Can't move opponent's piece!")

        moveValid, consequences = piece.validateMove(board=self, target=target)
        
        if not moveValid:
            raise MoveError("Piece cannot move there!")

        # Inefficient implementation
        tmpBoardstate = copy.deepcopy(self.boardstate)

        targetPiece = self[target]
        if targetPiece is not None:
            self[target] = None
            self.pieces[targetPiece.color][GRAVEYARD].append(targetPiece)
            self.pieces[targetPiece.color][LIVING].remove(targetPiece)

        self[current], self[target] = None, self[current]

        if consequences is not None:
            # Execute consequences
            if consequences[1] is None:
                # Capture piece
                captured = self[consequences[0]]
                
                # Remove piece
                self[consequences[0]] = None

                # Update living and graveyard
                self.pieces[captured.color][GRAVEYARD].append(captured)
                self.pieces[captured.color][LIVING].remove(captured)
            else:
                # Move piece
                self[consequences[0]], self[consequences[1]] = self[consequences[1]], self[consequences[0]]

                # Update position
                piece0 = self[consequences[1]]
                piece1 = self[consequences[0]]

                if piece0 is not None:
                    piece0.position = consequences[1]
                if piece1 is not None:
                    piece1.position = consequences[0]

        piece.position = target
        piece.executeMove(self, current, consequences)

        if self.inCheck(self.toMove):
            # Moving player is in check -> invalid move
            self.boardState = tmpBoardstate
            raise MoveError("Move leaves king in check!")

        self.toMove = -self.toMove

    def interpretMove(self, moveStr):
        """
        Interpret move given in algebraic notation
        to internal (current, target) representation.
        """

        if moveStr == "O-O-O":
            kingPos = self.pieces[self.toMove][KING].position
            return kingPos, (kingPos[0], kingPos[1] - 2)
        elif moveStr == "O-O":
            kingPos = self.pieces[self.toMove][KING].position
            return kingPos, (kingPos[0], kingPos[1] + 2)

        names = {
                "K": King,
                "Q": Queen,
                "R": Rook,
                "B": Bishop,
                "N": Knight
        }

        candidates = self.pieces[self.toMove][LIVING]
        result = []

        offset = 0
        if moveStr[0].isupper():
            piece = names[moveStr[0]]
            offset = 1
        else:
            piece = Pawn

        # Finite state automata for parsing destination and departure
        positions = []
        amtPos = 0
        pos = ""
        for c in moveStr[offset:]:
            if c.isalpha():
                if c == "x":
                    # Delimits two positions, is always followed by
                    # an alpha char (file)
                    continue
                if amtPos > 0:
                    positions.append(pos)
                if amtPos == 2:
                    break
                amtPos += 1
                pos = c
            elif c.isdigit():
                if pos == "":
                    pos = c
                    amtPos += 1
                else:
                    pos += c
            else:
                break
        positions.append(pos)

        depRank, depFile = None, None

        if len(positions) == 2:
            target = toInternal(positions[1])
            # Parse disambiguation
            if len(positions[0]) == 2:
                # Current position uniqely defined
                current = toInternal(positions[0])
                return self[current].position, target
            elif len(positions[0]) == 1:
                if positions[0].isdigit():
                    depRank, tmp = toInternal("a" + positions[0])
                else:
                    tmp, depFile = toInternal(positions[0] + "1")
        else:
            target = toInternal(positions[0])
        
        for candidate in candidates:
            if type(candidate) is not piece:
                continue
            if depRank is not None:
                if candidate.position[0] != depRank:
                    continue
            if depFile is not None:
                if candidate.position[1] != depFile:
                    continue

            if candidate.validateMove(self, target)[0]:
                result.append(candidate)

        if len(result) == 0:
            raise MoveError(moveStr, "No piece can make that move!")
        elif len(result) > 1:
            raise MoveError(moveStr, "Ambigous move! Disambiguate by giving a departing rank or file.")

        return result[0].position, target



