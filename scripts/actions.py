from enum import Enum

class Actions(Enum) :
    LAUNCH        = 0
    LAND          = 1
    FORWARD       = 2
    RIGHT         = 3
    BACKWARDS     = 4
    LEFT          = 5
    DO_TASK       = 6 
    # ROTATE_RIGHT  = 5
    # ROTATE_LEFT   = 6
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