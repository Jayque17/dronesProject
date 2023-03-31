
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

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
z += 20
tello.go_xyz_speed_mid(x, y, z, 20, mid)

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
x +=50
tello.go_xyz_speed_mid(x, y, z, 20, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
y -=50
tello.go_xyz_speed_mid(x, y, z, 20, mid)
onMissionPad = not onMissionPad
        
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
y -=50
tello.go_xyz_speed_mid(x, y, z, 20, mid)
onMissionPad = not onMissionPad
        
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
x -=50
tello.go_xyz_speed_mid(x, y, z, 20, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
tello.flip_back()
tello.go_xyz_speed_mid(x, y, z, 20, mid)

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
x -=50
tello.go_xyz_speed_mid(x, y, z, 20, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
z += 20
tello.go_xyz_speed_mid(x, y, z, 20, mid)

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
x -=50
tello.go_xyz_speed_mid(x, y, z, 20, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
tello.flip_back()
tello.go_xyz_speed_mid(x, y, z, 20, mid)

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
x +=50
tello.go_xyz_speed_mid(x, y, z, 20, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
if z > minz:
    z -= 20
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
else:
    print("bah non")

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
x +=50
tello.go_xyz_speed_mid(x, y, z, 20, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
x +=50
tello.go_xyz_speed_mid(x, y, z, 20, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
y +=50
tello.go_xyz_speed_mid(x, y, z, 20, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
y +=50
tello.go_xyz_speed_mid(x, y, z, 20, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
if z > minz:
    z -= 20
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
else:
    print("bah non")

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
x -=50
tello.go_xyz_speed_mid(x, y, z, 20, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 20, mid)
    tello.go_xyz_speed_mid(x, y, minz, 20, mid)
    z = minz
tello.land()
onMissionPad = not onMissionPad
