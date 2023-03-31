
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

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
y +=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
x +=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
y -=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad
        
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
y -=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad
        
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
y -=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad
        
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
x -=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
x -=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
x -=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
y +=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
y +=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
y +=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
x +=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
y -=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad
        
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
y -=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad
        
if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
x +=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
y +=50
tello.go_xyz_speed_mid(x, y, z, 10, mid)
onMissionPad = not onMissionPad

if onMissionPad:
    mid = tello.get_mission_pad_id()
    x = y = 0
    tello.go_xyz_speed_mid(x, y, z, 10, mid)
    tello.go_xyz_speed_mid(x, y, minz, 10, mid)
    z = minz
tello.land()
onMissionPad = not onMissionPad
