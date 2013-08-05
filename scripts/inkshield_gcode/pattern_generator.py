#! /usr/bin/python3
from __future__ import absolute_import, division, print_function, unicode_literals
character = [
0b0000101010101010,
0b0000010101010101,
]
nozzleCount = 12
nozzleWidth = 3

printLength = [100.0, 100.0]

feedRate = 10000

heightDiff = (heightEnd - heightStart)/charCount
charSeperation = printLength/charCount - charLength

for heightIdx in range(0, charCount):
    height = heightIdx*heightDiff
    for charIdx, val in enumerate(character):
        if val:
            splotSpot = (charIdx/len(character))*charLength+heightIdx*printLength/charCount
            print("G1X"+str(splotSpot)+"Z"+str(height)+"F"+str(feedRate))
            print("M400")
            print("M700 P0 S"+str(val))
print("M84")
