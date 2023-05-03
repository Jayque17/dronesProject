import copy
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
        self.max_z = 5
        self.max_real_z = 225
        self.tmp_drones = []
        self.tmp_target = []

        self.start_pos = self.__coordinates_to_integers(start_pos)
        self.targets_pos = [
            self.__coordinates_to_integers(p) for p in targets_pos]
        self.visited_targets = []

        self.nb_drones = 1  # nb_drones
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
        self.block_size = (WINDOW_WIDTH // self.max_w, WINDOW_HEIGHT // 2 // self.max_h)

    def reset(self, seed=0, options=False):

        self.state = 0
        if options == False:
            if (seed > 0):
                self.drones = copy.deepcopy(self.tmp_drones)
                self.visited_targets = copy.deepcopy(self.tmp_target)
            else:
                self.launched_drones = []
                self.drone_pos = self.start_pos
                self.drones = [Drone(self.__integers_to_coordinates(
                self.start_pos)) for i in range(self.nb_drones)]
                self.visited_targets = []
                self.distance_to_targets = [distance_squared(self.__integers_to_coordinates(target), drone.pos) for target
                                        in self.targets_pos for drone in self.drones]
        else :
            self.tmp_drones = copy.deepcopy(self.drones)
            self.tmp_target = copy.deepcopy(self.visited_targets)
            self.drone_pos = self.__coordinates_to_integers(self.drones[0].pos)


        return self.drone_pos

    def __out_of_bounds(self, pos):
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

        reward = -10
        done = 0

        if not (0 <= action < self.NB_ACTIONS):
            return

        drone_id = action // len(Actions)
        self.drones[drone_id].battery -= 1
        tmp_pos = self.drones[drone_id].pos

        if self.mapping_actions[action % len(Actions)] == Actions.LAUNCH:
            if (not self.drones[drone_id].launched):
                self.drones[drone_id].launched = True
                reward = -20
                
                self.launched_drones.append(self.drones[drone_id])
            else:
                reward = -20

        elif self.mapping_actions[action % len(Actions)] == Actions.FORWARD:
            if (self.drones[drone_id].launched):
                self.drones[drone_id].forward()
                
            else:
                reward = -20

        elif self.mapping_actions[action % len(Actions)] == Actions.RIGHT:
            if (self.drones[drone_id].launched):
                self.drones[drone_id].right()
                
            else:
                reward = -20

        elif self.mapping_actions[action % len(Actions)] == Actions.BACKWARDS:
            if (self.drones[drone_id].launched):
                self.drones[drone_id].backward()
                
            else:
                reward = -20

        elif self.mapping_actions[action % len(Actions)] == Actions.LEFT:
            if (self.drones[drone_id].launched):
                self.drones[drone_id].left()
                
            else:
                reward = -20

        elif self.mapping_actions[action % len(Actions)] == Actions.UP:
            print("up")
            if (self.drones[drone_id].launched):
                # PrintInDroneFile
                self.drones[drone_id].up()
            else:
                reward = -20

        elif self.mapping_actions[action % len(Actions)] == Actions.DOWN:
            print("down")
            if (self.drones[drone_id].launched):
                # PrintInDroneFile
                self.drones[drone_id].down()
            else:
                reward = -20

        elif self.mapping_actions[action % len(Actions)] == Actions.DO_TASK:
            if self.drones[drone_id].launched:
                if self.drone_pos in self.targets_pos and self.drone_pos not in self.visited_targets:
                   
                    reward = 100
                    done = 1
                    self.visited_targets.append(self.drone_pos)
                else:
                    reward = -200
            else:
                reward = -200

        elif self.mapping_actions[action % len(Actions)] == Actions.LAND:
            if sorted(self.targets_pos) == sorted(self.visited_targets) and self.drone_pos == self.start_pos:
                done = 2
                reward = 500
            if (self.drones[drone_id] in self.launched_drones):
                self.launched_drones.remove(self.drones[drone_id])
                self.drones[drone_id].launched = False
               
            else:
                reward = -50

        if (self.__out_of_bounds(self.drones[drone_id].pos)) or self.drones[drone_id].pos in [(p[0], p[1]) for p in
                                                                                              self.obstacles_pos]:
            self.drones[drone_id].pos = tmp_pos
            reward = -100

        if sorted(self.targets_pos) == sorted(self.visited_targets) and self.drone_pos == self.start_pos and self.mapping_actions[action % len(Actions)] == Actions.LAND:
            done = 2
            reward += 500

        if self.drones[drone_id].battery <= 0:
            reward = -100
            done = 2

        self.drone_pos = self.__coordinates_to_integers(
            self.drones[drone_id].pos)
        return self.drone_pos, reward, done, {}

    def __draw_grid(self):
        for y in range(0, self.max_h):
            for x in range(0, self.max_w):
                rect = pygame.Rect(x * self.block_size[0], y * self.block_size[1], self.block_size[0],
                                   self.block_size[1])
                pygame.draw.rect(self.screen, self.black, rect, 1)

    def __draw_qtable(self, Qtable):
        for y in range(0, self.max_h):
            for x in range(0, self.max_w):
                n = np.argmax(Qtable[self.__coordinates_to_integers((x, y))])
                drone_id = n // len(Actions)
                action = Actions(n % len(Actions))

                rect = pygame.Rect(x * self.block_size[0], WINDOW_HEIGHT // 2 +
                                   y * self.block_size[1], self.block_size[0], self.block_size[1])
                pygame.draw.rect(self.screen, self.black, rect, 1)

                colors = [pygame.Color(255, 0, 0), pygame.Color(255, 255, 0), pygame.Color(0, 255, 0), pygame.Color(
                    0, 255, 255), pygame.Color(0, 0, 255), pygame.Color(255, 0, 255), pygame.Color(255, 0, 0)]

                if action in [Actions.BACKWARDS, Actions.FORWARD, Actions.LEFT, Actions.RIGHT]:
                    self.screen.blit(pygame.transform.rotate(self.scaled_arrow, 90. * (
                            action.value % 4)), (x * self.block_size[0], WINDOW_HEIGHT // 2 + y * self.block_size[1]))
                elif action in [Actions.LAUNCH, Actions.LAND, Actions.DO_TASK]:
                    pygame.draw.circle(self.screen, colors[action.value % 4],
                                       (x * self.block_size[0] + self.block_size[0] //
                                        2, WINDOW_HEIGHT // 2 + y * self.block_size[1] + self.block_size[1] // 2),
                                       self.block_size[1] // 2)

                pygame.draw.circle(self.screen, (255, 195, 0),
                                   (self.drones[0].pos[0] * self.block_size[0] + self.block_size[0] //
                                    2,
                                    WINDOW_HEIGHT // 2 + self.drones[0].pos[1] * self.block_size[1] + self.block_size[
                                        1] // 2), self.block_size[1] // 8)

        pygame.draw.line(self.screen, (255, 0, 0), (0, WINDOW_HEIGHT // 2), (WINDOW_WIDTH, WINDOW_HEIGHT // 2), 15)


    def __draw_obstacle(self, obstacle_pos):

        alt_color = (255, 195, 0)
        for i in range(0, self.block_size[1]):
            for j in range(0, self.block_size[0]):
                if ((i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0)):
                    rect = pygame.Rect(
                        obstacle_pos[0] * self.block_size[0] + j, obstacle_pos[1] * self.block_size[1] + i, 1, 1)
                    pygame.draw.rect(self.screen, self.black, rect, 1)
        if (str(obstacle_pos[2]) != '0' and self.font_simu != None):
            text_obstacle = self.font_simu.render(
                obstacle_pos[2], True, alt_color)
            self.screen.blit(
                text_obstacle, (obstacle_pos[0] * self.block_size[0], obstacle_pos[1] * self.block_size[1]))


    def __draw_target(self):
        target_col = (0, 255, 0)
        for target in self.targets_pos:
            if target not in self.visited_targets:
                target_pos = self.__integers_to_coordinates(target)
                pygame.draw.circle(self.screen, target_col, (target_pos[0] * self.block_size[0] + (
                        self.block_size[0] - 1) / 2, target_pos[1] * self.block_size[1] + (self.block_size[1] - 1) / 2),
                                   self.block_size[0] / 2, 5)


    def __draw_house(self):
        col_wall = (255, 228, 225)
        col_door = (165, 42, 42)
        col_roof = (255, 0, 0)

        start = self.__integers_to_coordinates(self.start_pos)
        wall = pygame.Rect(start[0] * self.block_size[0] + (1 / 5) * self.block_size[0],
                           start[1] * self.block_size[1] + (2 / 3) * self.block_size[1],  self.block_size[0], self.block_size[1]//3)
        door = pygame.Rect(start[0] * self.block_size[0] + (1 / 2) * self.block_size[0],
                           start[1] * self.block_size[1] + (5 / 6) * self.block_size[1], 2, 5)

        start_roof = (start[0] * self.block_size[0] + (1 / 2) *
                      self.block_size[0], start[1] * self.block_size[1])
        roof_b = (start[0] * self.block_size[0] + self.block_size[0],
                  start[1] * self.block_size[1] + (2 / 3) * self.block_size[1])
        roof_c = (start[0] * self.block_size[0], start[1] *
                  self.block_size[1] + (2 / 3) * self.block_size[1])

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
            arrow = pygame.Surface((350, 350), pygame.SRCALPHA, 32)
            pygame.draw.polygon(arrow, (0, 0, 0), ((
                                                       25, 125), (25, 225), (225, 225), (225, 325), (325, 175),
                                                   (225, 25), (225, 125)))
            self.scaled_arrow = pygame.transform.scale(
                arrow, self.block_size)
        if self.clock is None:
            self.clock = pygame.time.Clock()
        if self.font_simu is None:
            self.font_simu = pygame.font.SysFont(
                'liberationmono', self.block_size[1], True)

        self.screen.fill(self.white)
        self.__draw_grid()
        self.__draw_house()
        self.__draw_qtable(Qtable)

        for i in range(len(self.obstacles_pos)):
            self.__draw_obstacle(self.obstacles_pos[i])
        for i in range(len(self.drones)):
            self.drones[i].draw_drone(self.screen, self.block_size)
        self.__draw_target()
    
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.clock.tick(1)
