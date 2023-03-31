from managerEnv import ManagerEnv

def parser(file_ap):
    f = open(file_ap, "r")
    elems = f.readlines()
    for i in range(len(elems)):
        if elems[i][-1] == "\n":
            elems[i] = elems[i][:-1]
    nb_drones = int(elems[0])
    map_meter = elems[1].split()
    map_width_meter = float(map_meter[0])
    map_height_meter = float(map_meter[1])
    nb_items = 0

    targets_pos = []
    obstacles_pos = []
    l = None
    for i in range(2, len(elems)):
        l = elems[i].split()
        if (len(l) >= 3):
            nb_items += 1
            if (l[0] == "H"):
                start_pos = (int(l[1]), int(l[2]))
            elif (l[0] == "T"):
                targets_pos.append((int(l[1]), int(l[2])))
            else:
                raise Exception("unhandle parameter: " + l[0])
        elif (len(l) == 1):
            for j in range(len(l[0])):
                if (l[0][j] == "x"):
                    obstacles_pos.append((j, i - 2 - nb_items, 0))
                elif (l[0][j] in "0123456789ABCDEF"):
                    if (l[0][j] != "0"):
                        obstacles_pos.append((j, i - 2 - nb_items,  l[0][j]))
                else:
                    raise Exception("unhandle parameter: " + l[0][j])
    map_simu_dims = (len(l[0]), len(elems) - nb_items - 2)
    map_real_dims = (map_width_meter, map_height_meter)

    return ManagerEnv(nb_drones, map_real_dims, map_simu_dims, start_pos, targets_pos, obstacles_pos)


def writeActionsToPythonScript(listActions, filePathName, map_real_dims, map_simu_dims):

    block_w = int(map_real_dims[0] // map_simu_dims[0])
    block_h = int(map_real_dims[1] // map_simu_dims[1])

    print("block_w: " + str(block_w))
    print("block_h: " + str(block_h))

    with open(filePathName, "w") as f:
        f.write(
            """
from djitellopy import Tello
tello = Tello()
tello.connect()
tello.enable_mission_pads()
onMissionPad = True
minz = 50
x = 0
y = 0
z = minz
mid = -1

print("temperature", tello.get_temperature())
print("battery ", tello.get_battery())

tello.takeoff()
print("temperature", tello.get_temperature())
print("battery ", tello.get_battery())
"""
        )

        for a in listActions: 
            if a == 0:  # Right 
                f.write(
                    """
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
y -=""" + str(block_w) + """
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad
        """
                )
            elif a == 1:  # Backward 
                f.write(
                    """
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
x -=""" + str(block_h) + """
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad
"""
                )
            elif a == 2:  # Left 
                f.write(
                    """
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
y +=""" + str(block_w) + """
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad
"""
                )
            elif a == 3:  # Forward 
                f.write(
                    """
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
x +=""" + str(block_h) + """
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad
"""
                )
            elif a == 4:  # Launch 
                f.write(
                    """
tello.land()
z = minz
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad
"""
                )
            elif a == 5:  # Land 
                f.write(
                    """
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
    tello.go_xyz_speed_mid(x, y, minz, 10, mid)
    z = minz
tello.land()
onMissionPad = not onMissionPad
"""
                )
            elif a == 6:  # Do Task 
                f.write(
                    """
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
tello.flip_back()
tello.go_xyz_speed_mid(x, y, z, 10, mid)
"""
                )
            elif a == 7:  # Up 
                f.write(
                    """
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
z += 20
tello.go_xyz_speed_mid(x, y, z, 10, mid)
"""
                )
            elif a == 8:  # Down 
                f.write(
                    """
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
if z > minz:
    z -= 20
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
else:
    print("bah non")
"""
                )
            else:
                raise ValueError(
                    "This action id isn't handle, your action id is " + a + ", it only from 0 to 8!")
