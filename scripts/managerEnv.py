import pygame
import numpy as np
import cv2
import time 

import gym
from gym import Env
from gym.spaces import Discrete, Box, MultiDiscrete, Dict

#from google.colab.patches import cv2_imshow
#from google.colab import output

from drone import Drone
from actions import Actions

WINDOW_HEIGHT = 768
WINDOW_WIDTH = 1024
block_size = 30
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
font_simu = pygame.font.SysFont('liberationmono', block_size, True)

class ManagerEnv(Env):
  def __init__(self, nb_drones, map_real_dims, map_simu_dims, start_pos, targets_pos, obstacles_pos) -> None:
    self.action_space = Discrete(len(Actions) * nb_drones,)

    self.max_op = 100
    self.state = 0
    self.nb_drones = nb_drones
    self.drones = [Drone(start_pos) for i in range(nb_drones)]
    self.map_real_dims = map_real_dims
    self.map_simu_dims = map_simu_dims
    self.start_pos = start_pos
    self.targets_pos = targets_pos
    self.obstacles_pos = obstacles_pos
    self.launched_drones = []
    self.visited_targets = []
    self.max_w = map_simu_dims[0]
    self.max_h = map_simu_dims[1]

    low = np.zeros((2,), dtype=int)
    high = np.array([self.nb_drones, len(self.targets_pos)])

    # self.observation_space = Dict(
    #     {
    #         "drones": Box(0, len(self.drones), shape=(2,), dtype=int),
    #         "target": Box(0, len(self.targets_pos), shape=(3,), dtype=int),
    #         "obstacle": Box(0, len(self.obstacles_pos), shape=(3,), dtype=int),
    #     }
    # )

    self.observation_space = Dict(
        {
            "drones": Box(0, len(self.drones), shape=(2,), dtype=int),
            "target": Box(0, len(self.targets_pos), shape=(3,), dtype=int),
            "obstacle": Box(0, len(self.obstacles_pos), shape=(3,), dtype=int),
        }
    )

    self.WINDOW_HEIGHT = 768
    self.WINDOW_WIDTH = 1024
    self.MAP_HEIGHT = 750
    self.MAP_WIDTH = 1020
    
    self.done = False
    self.white = (255, 255, 255)
    self.block_size = 30 # in pixelss
    self.wait_time = 0.5 # in seconds
          
  
  def _get_obs(self) : 
    # return np.ndarray([
    #   np.array(self.obstacles_pos, numpy.dtype('int, int')),
    #   np.array(self.targets_pos),
    #   np.array([drone.pos for drone in self.drones])  
    # ], )
    a = np.ndarray([drone.pos for drone in self.drones], dtype='object')
    print("baba", a)
    d = Dict(
        {
            "drones": np.ndarray([drone.pos for drone in self.drones], dtype='object'),
            "target": np.ndarray(self.targets_pos, dtype='object'),
            "obstacle": np.ndarray(self.obstacles_pos, dtype='object'),
        }
    )

    print('jolie dico', d)
    return d
  
  def out_of_bounds(self, pos, max_h, max_w):
    if (pos[0] < 0 or pos[0] > max_w):
        return False
    if (pos[1] < 0 or pos[1] > max_h):
        return False
    return True
  
  def step(self, action):
    print("coucou c moi step")
    self.max_op -= 1
    reward = -1
    done = False

    if (not self.action_space.contains(action)):
      return

    drone_id = action // len(Actions)
    action_id = Actions(action % len(Actions))

    print("drone :", drone_id, "fait", action_id)

    if action_id == Actions.LAUNCH:
      if(not self.drones[drone_id].launched):
        self.drones[drone_id].launched = True
        reward = -10
        #PrintInDroneFile
        self.launched_drones.append(self.drones[drone_id])

    tmp_pos = self.drones[drone_id].pos

    if action_id == Actions.FORWARD:
      if(self.drones[drone_id].launched):
        self.drones[drone_id].forward()
        #PrintInDroneFile
        reward = 1

    if action_id == Actions.RIGHT:
      if(self.drones[drone_id].launched):
        self.drones[drone_id].right()
        #PrintInDroneFile
        reward = 1

    if action_id == Actions.BACKWARDS:
      if(self.drones[drone_id].launched):
        self.drones[drone_id].backward() 
        #PrintInDroneFile
        reward = 1
        
    if action_id == Actions.LEFT:
      if(self.drones[drone_id].launched):
        self.drones[drone_id].left()
        #PrintInDroneFile
        reward = 1
        
    if action_id == Actions.ROTATE_RIGHT:
      if(self.drones[drone_id].launched):
        self.drones[drone_id].rotate(1)
        #PrintInDroneFile
        reward = 1

    if action_id == Actions.ROTATE_LEFT:
      if(self.drones[drone_id].launched):
        self.drones[drone_id].rotate(-1)
        #PrintInDroneFile
        reward = 1

    if action_id == Actions.UP:
      if(self.drones[drone_id].launched):
        #PrintInDroneFile
        self.drones[drone_id].up()
        reward = 1

    if action_id == Actions.DOWN:
      if(self.drones[drone_id].launched):
        #PrintInDroneFile
        self.drones[drone_id].down()
        reward = 1

    if action_id == Actions.DO_TASK:
      if(self.drones[drone_id].launched):
        if (self.drones[drone_id].pos in self.targets_pos and self.drones[drone_id].pos not in self.visited_targets):
          #PrintInDroneFile
          reward = 50
          self.visited_targets.append(self.drones[drone_id].pos)
    
    if action_id == Actions.LAND:
      if (self.drones[drone_id].pos == self.start_pos):
        if (self.drones[drone_id] in self.launched_drones):
          self.launched_drones.remove(self.drones[drone_id])
          #PrintInDroneFile
          reward = 1

    if (self.out_of_bounds(self.drones[drone_id].pos, self.max_w, self.max_h) or self.drones[drone_id].pos in [(p[0],p[1]) for p in self.obstacles_pos]):
      self.drones[drone_id].pos = tmp_pos
      reward = -1

    elif (self.drones[drone_id].battery <= 0):
      print("Battery done")
      reward = -100
      done = True
        
    if not self.targets_pos and not self.launched_drones :
      "Targets done"
      done = True
      reward = 100

    if (self.max_op <= 0):
      "Maxop done"
      done = True
    print(self.drones[drone_id].pos)
    return (self._get_obs(), reward, done, False, {})


  def _lie_to_env(observation_space): #i don't understand
    pass


  def __draw_grid(self):
    black = (0, 0, 0)
    for x in range(0, self.MAP_WIDTH, self.block_size):
      for y in range(0, self.MAP_HEIGHT, self.block_size):
        rect = pygame.Rect(x, y, self.block_size, self.block_size)
        pygame.draw.rect(screen, black, rect, 1)


  def __draw_obstacle(self, obstacle_pos):
    black = (0, 0, 0)
    alt_color = (255, 195,0)
    for i in range(0, self.block_size):
      for j in range(0, self.block_size):
        if((i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0)):
          rect = pygame.Rect(obstacle_pos[0] * self.block_size + j, obstacle_pos[1] * self.block_size + i, 1, 1)
          pygame.draw.rect(screen, black, rect, 1)
    if(int(obstacle_pos[2]) > 0 and font_simu != None):
      text_obstacle = font_simu.render(str(obstacle_pos[2]), True, alt_color)
      screen.blit(text_obstacle, (obstacle_pos[0] * self.block_size, obstacle_pos[1] * self.block_size))

  def __draw_target(self, target_pos):
    target_col = (0, 255, 0)
    if(not target_pos[2]):
      pygame.draw.circle(screen, target_col, (target_pos[0] * self.block_size + (self.block_size - 1)/2, target_pos[1] * self.block_size + (self.block_size - 1)/2), self.block_size/2, 5)
  

  def __draw_house(self):
    col_wall = (255,228,225)
    col_door = (165,42,42)
    col_roof = (255,0,0)
    
    wall = pygame.Rect(self.start_pos[0] * self.block_size + (1/5) * self.block_size, self.start_pos[1] * self.block_size  + (2/3) * self.block_size, 20, 10)
    door = pygame.Rect(self.start_pos[0] * self.block_size + (1/2) * self.block_size, self.start_pos[1] * self.block_size  + (5/6) * self.block_size, 2, 5)

    start_roof = (self.start_pos[0] * self.block_size + (1/2) * self.block_size, self.start_pos[1] * self.block_size)
    roof_b = (self.start_pos[0] * self.block_size + self.block_size, self.start_pos[1] * self.block_size + (2/3) * self.block_size)
    roof_c = (self.start_pos[0] * self.block_size, self.start_pos[1] * self.block_size + (2/3) * self.block_size)
    
    pygame.draw.polygon(screen, col_roof, (start_roof,roof_b,roof_c))
    pygame.draw.rect(screen, col_wall, wall)
    pygame.draw.rect(screen, col_door, door)
  
  
  def render(self):
    screen.fill(self.white)
    self.__draw_grid()
    self.__draw_house()

    for i in range(len(self.obstacles_pos)):
      self.__draw_obstacle(self.obstacles_pos[i])
    for i in range(len(self.targets_pos)):
      self.__draw_target(self.targets_pos[i])
    for i in range(len(self.drones)):
      self.drones[i].draw_drone(screen, self.block_size)

    view = pygame.surfarray.array3d(screen)
    view = view.transpose([1, 0, 2])
    img_bgr = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
    cv2.imshow(img_bgr)
    time.sleep(self.wait_time)
    

  def reset(self):
    self.state = 0
    self.launched_drones = []
    self.nb_drones = self.nb_drones
    self.drones = [Drone(self.start_pos) for i in range(self.nb_drones)] 
    # print(self._get_obs())
    # return (self._get_obs(), {})
    return(self._get_obs(), {})

def parser(file_ap):
  f = open(file_ap, "r")
  elems = f.readlines()
  for i in range(len(elems)):
    if elems[i][-1] == "\n":
      elems[i] = elems[i][:-1]
  nb_drones = int(elems[0][0])
  map_meter = elems[1].split()
  map_width_meter = float(map_meter[0])
  map_height_meter = float(map_meter[1])
  nb_items = 0

  targets_pos = []
  obstacles_pos = []
  l = None
  for i in range(2, len(elems)):
    l = elems[i].split() 
    if(len(l) >= 3):
      nb_items += 1
      if(l[0] == "H"):
        start_pos = (int(l[1]), int(l[2]))
      elif(l[0] == "T"):
        targets_pos.append((int(l[1]), int(l[2]), False))
      else:
        raise Exception("unhandle parameter: " + l[0])
    elif(len(l) == 1):
      for j in range(len(l[0])):
        if(l[0][j] == "x"):
          obstacles_pos.append((j,i - 2 - nb_items , 0))
        elif(l[0][j] in "0123456789ABCDEF"):
          if(l[0][j] != "0"):
            obstacles_pos.append((j,i - 2 - nb_items,  l[0][j]))
        else:
          raise Exception("unhandle parameter: " + l[0][j])        
  map_simu_dims = (len(l[0]), len(elems) - nb_items - 2)
  map_real_dims = (map_width_meter, map_height_meter)

  return ManagerEnv(nb_drones, map_real_dims, map_simu_dims, start_pos, targets_pos, obstacles_pos)

