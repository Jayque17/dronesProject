from djitellopy import Tello
from time import sleep

tello = Tello()

tello.connect()
tello.enable_mission_pads()
tello.takeoff()# 90
print("temperature", tello.get_temperature())
print("battery ", tello.get_battery())

print("id = ", tello.get_mission_pad_id())
print("hauteur par rapport au pad = ", tello.get_mission_pad_distance_z())
print("hauteur absolue = ", tello.get_height())

# tello.go_xyz_speed_mid(100, 0, 90, 20, 1)
# tello.go_xyz_speed_mid(100, 0, 90, 20, 2)
# tello.go_xyz_speed_mid(100, 0, 90, 20, 3)
# tello.go_xyz_speed_mid(0, -120, 180, 20, 4) # Y positif à gauche
# tello.go_xyz_speed_mid(0, 0, 50, 10, 7)


# tello.go_xyz_speed_mid(0, 0, 50, 10, 4)
tello.go_xyz_speed_mid(100, 0, 0, 10, tello.get_mission_pad_id())

tello.go_xyz_speed_mid(100, 0, 0, 10, tello.get_mission_pad_id())
tello.go_xyz_speed_mid(0, 0, 80, 10, tello.get_mission_pad_id())
# tello.go_xyz_speed_mid(0, 0, 60, 10, tello.get_mission_pad_id())
# tello.go_xyz_speed_mid(0, 0, 110, 10, tello.get_mission_pad_id())
# tello.go_xyz_speed_mid(0, -120, 110, 10, tello.get_mission_pad_id())
# tello.go_xyz_speed_mid(0, 0, 50, 10, tello.get_mission_pad_id())




# tello.go_xyz_speed_mid(100, 0, 180, 20, 5)


tello.land()