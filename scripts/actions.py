from enum import Enum

class Actions(Enum) :
    LAUNCH        = 0
    FORWARD       = 1
    RIGHT         = 2
    BACKWARDS     = 3
    LEFT          = 4
    ROTATE_RIGHT  = 5
    ROTATE_LEFT   = 6
    UP            = 7
    DOWN          = 8
    DO_TASK       = 9 
    LAND          = 10

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