import sys
import pygame
import numpy as np

from drone import Drone
from actions import Actions

WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800

def distance_squared(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return (x1 - x2) ** 2 + (y1 - y2) ** 2

class ManagerEnv(object):
    def __init__(self, nb_drones, map_real_dims, map_simu_dims, start_pos, targets_pos, obstacles_pos) -> None:

        self.map_real_dims = map_real_dims
        self.map_simu_dims = map_simu_dims

        self.max_w = self.map_simu_dims[0]
        self.max_h = self.map_simu_dims[1]

        self.start_pos = self.__coordinates_to_integers(start_pos)
        self.targets_pos = [self.__coordinates_to_integers(p) for p in targets_pos]
        self.visited_targets = []
    
        self.nb_drones = 2#nb_drones
        # self.battery_actions = 100
        self.drones = [Drone(start_pos) for i in range(self.nb_drones)]
        self.drone_pos = self.__coordinates_to_integers(self.drones[0].pos)
        self.launched_drones = []
        
        self.obstacles_pos = obstacles_pos
        
        self.NB_ACTIONS = len(Actions) * self.nb_drones
        self.mapping_actions = dict((item.value, item) for item in Actions)
        self.NB_STATES = self.max_w * self.max_h

        self.screen = None
        self.clock = None
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.font_simu = None
        self.block_size = WINDOW_WIDTH//2//self.max_w

    def reset(self, seed=None, options=None):

        self.state = 0
        self.launched_drones = []
        # self.nb_drones = self.nb_drones
        # self.drones = [Drone(self.start_pos) for i in range(self.nb_drones)]
        self.drone_pos = self.start_pos
        self.drones = [Drone(self.__integers_to_coordinates(self.start_pos)) for i in range(self.nb_drones)]
        self.visited_targets = []
        # self.battery_actions = 1000
        
        self.distance_to_targets = [distance_squared(self.__integers_to_coordinates(target), drone.pos) for target in self.targets_pos for drone in self.drones]
        return self.drone_pos

    def __out_of_bounds(self, pos):
        # print("pos", pos, "max_w", self.max_w, "max_h", self.max_h)
        x, y = pos
        return (x < 0 or x >= self.max_w or y < 0 or y >= self.max_h)

    def __coordinates_to_integers(self, coordinates):
        """ Takes a tuple of coordinates and returns the corresponding integer """
        x, y = coordinates
        return y * self.max_w + x

    def __integers_to_coordinates(self, integer):
        """ Takes an integer and returns the corresponding coordinates """
        x = integer % self.max_w
        y = integer // self.max_w
        return (x, y)

    def step(self, action):
        # print('battery=', self.battery_actions)
        # self.battery_actions -= 1

        reward = -1
        done = False

        if not (0 <= action < self.NB_ACTIONS):
            return

        drone_id = action // len(Actions)
        self.drones[drone_id].battery -= 1
        # drone_id = 0
        tmp_pos = self.drones[drone_id].pos
        # print("tmp_pos", tmp_pos)

        if self.mapping_actions[action % len(Actions)] == Actions.LAUNCH:
            # print("launch")
            if (not self.drones[drone_id].launched):
                self.drones[drone_id].launched = True
                reward = -10
                # PrintInDroneFile
                self.launched_drones.append(self.drones[drone_id])
            else:
                reward = -20

        elif self.mapping_actions[action % len(Actions)] == Actions.FORWARD:
            # print("forward")
            if (self.drones[drone_id].launched):
                self.drones[drone_id].forward()
                # PrintInDroneFile
            else:
                reward = -20

        elif self.mapping_actions[action % len(Actions)] == Actions.RIGHT:
            # print("right")
            if (self.drones[drone_id].launched):
                self.drones[drone_id].right()
                # PrintInDroneFile
            else:
                reward = -20

        elif self.mapping_actions[action % len(Actions)] == Actions.BACKWARDS:
            # print("backwards")
            if (self.drones[drone_id].launched):
                self.drones[drone_id].backward()
                # PrintInDroneFile
            else:
                reward = -20

        elif self.mapping_actions[action % len(Actions)] == Actions.LEFT:
            # print("left")
            if (self.drones[drone_id].launched):
                self.drones[drone_id].left()
                # PrintInDroneFile
            else:
                reward = -20

        # elif self.mapping_actions[action % len(Actions)] == Actions.ROTATE_RIGHT:
        #     print("rotate right")
        #     if (self.drones[drone_id].launched):
        #         self.drones[drone_id].rotate(1)
        #         reward = -15
        #         # PrintInDroneFile
        #     else:
        #         reward = -20

        # elif self.mapping_actions[action % len(Actions)] == Actions.ROTATE_LEFT:
        #     print("rotate left")
        #     if (self.drones[drone_id].launched):
        #         self.drones[drone_id].rotate(-1)
        #         reward = -15
        #         # PrintInDroneFile
        #     else:
        #         reward = -20

        # elif self.mapping_actions[action % len(Actions)] == Actions.UP:
        #     print("up")
        #     if (self.drones[drone_id].launched):
        #         # PrintInDroneFile
        #         self.drones[drone_id].up()
        #     else:
        #         reward = -20

        # elif self.mapping_actions[action % len(Actions)] == Actions.DOWN:
        #     print("down")
        #     if (self.drones[drone_id].launched):
        #         # PrintInDroneFile
        #         self.drones[drone_id].down()
        #     else:
        #         reward = -20

        elif self.mapping_actions[action % len(Actions)] == Actions.DO_TASK:
            # print("do task")
            if (self.drones[drone_id].launched):
                if (self.drone_pos in self.targets_pos and self.drone_pos not in self.visited_targets):
                    # PrintInDroneFile
                    reward = 5000
                    self.visited_targets.append(self.drone_pos)
                else:
                    reward = -10
            else:
                reward = -20

        elif self.mapping_actions[action % len(Actions)] == Actions.LAND:
            # print("land")
            if (self.drones[drone_id] in self.launched_drones):
                self.launched_drones.remove(self.drones[drone_id])
                # PrintInDroneFile
            else:
                reward = -50

        
        if (self.__out_of_bounds(self.drones[drone_id].pos)) or self.drones[drone_id].pos in [(p[0],p[1]) for p in self.obstacles_pos]:
            # print("Out of bounds", tmp_pos, self.drones[drone_id].pos)
            self.drones[drone_id].pos = tmp_pos
            done = True
            reward = -100

        elif (self.drones[drone_id].battery <= 0):
          #print("Battery done")
          reward = -100
          done = True

        elif sorted(self.targets_pos) == sorted(self.visited_targets) and self.drone_pos == self.start_pos:
            # Targets done
            # print("Targets done")
            done = True
            reward = 100

        # elif (self.battery_actions <= 0):
        #     # Battery outOfOrder
        #     # print("Battery outOfOrder")
        #     reward = -100
        #     done = True
        
        # reward drone if it gets closer to one of the targets
        last_distance = self.distance_to_targets
        self.distance_to_targets = [distance_squared(self.__integers_to_coordinates(target), drone.pos) for target in self.targets_pos for drone in self.drones]
        if last_distance > self.distance_to_targets:
            reward += 5


        self.drone_pos = self.__coordinates_to_integers(self.drones[drone_id].pos)
        return (self.drone_pos, reward, done, {})


    def __draw_grid(self):
        for x in range(0, WINDOW_WIDTH, self.block_size):
            for y in range(0, WINDOW_HEIGHT//2, self.block_size):
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, self.black, rect, 1)
    
    def __draw_qtable(self, Qtable):
        for y in range(0, self.max_h):
            for x in range(0, self.max_w):
                rect = pygame.Rect(x * self.block_size, WINDOW_HEIGHT//2 + 10 + y * self.block_size, self.block_size, self.block_size)
                pygame.draw.rect(self.screen, self.black, rect, 1)

                text_Qtable = self.font_simu.render(
                    str(np.argmax(Qtable[self.__coordinates_to_integers((x,y))])), 
                    True, 
                    (255,0,0)
                )
                self.screen.blit(
                text_Qtable, 
                (x * self.block_size, 
                 WINDOW_HEIGHT//2 + 10 + y * self.block_size))





    def __draw_obstacle(self, obstacle_pos):

        alt_color = (255, 195, 0)
        for i in range(0, self.block_size):
            for j in range(0, self.block_size):
                if ((i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0)):
                    rect = pygame.Rect(
                        obstacle_pos[0] * self.block_size + j, obstacle_pos[1] * self.block_size + i, 1, 1)
                    pygame.draw.rect(self.screen, self.black, rect, 1)
        if (int(str(obstacle_pos[2]), base=16) > 0 and self.font_simu != None):
            text_obstacle = self.font_simu.render(
                str(obstacle_pos[2]), True, alt_color)
            self.screen.blit(
                text_obstacle, (obstacle_pos[0] * self.block_size, obstacle_pos[1] * self.block_size))

    def __draw_target(self):
        target_col = (0, 255, 0)
        for target in self.targets_pos:
            if target not in self.visited_targets :
                target_pos = self.__integers_to_coordinates(target)
                pygame.draw.circle(self.screen, target_col, (target_pos[0] * self.block_size + (
                    self.block_size - 1)/2, target_pos[1] * self.block_size + (self.block_size - 1)/2), self.block_size/2, 5)

    def __draw_house(self):
        col_wall = (255, 228, 225)
        col_door = (165, 42, 42)
        col_roof = (255, 0, 0)

        start = self.__integers_to_coordinates(self.start_pos)
        wall = pygame.Rect(start[0] * self.block_size + (1/5) * self.block_size,
                           start[1] * self.block_size + (2/3) * self.block_size, 20, 10)
        door = pygame.Rect(start[0] * self.block_size + (1/2) * self.block_size,
                           start[1] * self.block_size + (5/6) * self.block_size, 2, 5)

        start_roof = (start[0] * self.block_size + (1/2) *
                      self.block_size, start[1] * self.block_size)
        roof_b = (start[0] * self.block_size + self.block_size,
                  start[1] * self.block_size + (2/3) * self.block_size)
        roof_c = (start[0] * self.block_size, start[1] *
                  self.block_size + (2/3) * self.block_size)

        pygame.draw.polygon(self.screen, col_roof,
                            (start_roof, roof_b, roof_c))
        pygame.draw.rect(self.screen, col_wall, wall)
        pygame.draw.rect(self.screen, col_door, door)

    def render(self, Qtable=None):

        if self.screen is None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode(
                (WINDOW_WIDTH, WINDOW_HEIGHT))
        if self.clock is None:
            self.clock = pygame.time.Clock()
        if self.font_simu is None:
            self.font_simu = pygame.font.SysFont('liberationmono', self.block_size, True)

        self.screen.fill(self.white)
        self.__draw_grid()
        self.__draw_house()
        # if(Qtable == None):
        self.__draw_qtable(Qtable)

        for i in range(len(self.obstacles_pos)):
            self.__draw_obstacle(self.obstacles_pos[i])
        for i in range(len(self.drones)):
          self.drones[i].draw_drone(self.screen, self.block_size)

        self.__draw_target()
        # self.drones[0].draw_drone(self.screen, self.block_size)

        # view = pygame.surfarray.array3d(screen)
        # view = view.transpose([1, 0, 2])
        # img_bgr = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
        # cv2.imshow(img_bgr)
        # time.sleep(self.wait_time)

        # canvas = pygame.Surface((self.window_size, self.window_size))
        # canvas.fill((255, 255, 255))
        # self.window.blit(canvas, canvas.get_rect())

        pygame.event.pump()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.clock.tick(0.8)
