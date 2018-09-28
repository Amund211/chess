#! /usr/bin/env python

__all__ = ["NotationError", "MoveError", "StateError"]


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



