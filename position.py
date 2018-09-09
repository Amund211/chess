#! /usr/bin/env python

def toInternal(square):
    _file, rank = square.lower()
    inFile = ord(_file) - 97
    inRank = int(rank) - 1

    return inRank, inFile


def toHuman(position):
    huFile = chr(position[1] + 97)
    huRank = str(position[0] + 1)

    return huFile + huRank
