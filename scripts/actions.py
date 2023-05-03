from enum import Enum

class Actions(Enum) :
    RIGHT         = 0
    BACKWARDS     = 1
    LEFT          = 2
    FORWARD       = 3
    LAUNCH        = 4
    LAND          = 5
    DO_TASK       = 6 
    # UP            = 7
    # DOWN          = 8


""" 
Different possible actions :
0 - SpawnDrone
1 - Forward
2 - Right
3 - Backwards
4 - Left
5 - Rotate Right
6 - Rotate Left
7 - Up
8 - Down
9 - Do task
10 - Land
"""