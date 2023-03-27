import pygame
from gym.spaces import Discrete

from drone import Drone
from actions import Actions

WINDOW_HEIGHT = 768
WINDOW_WIDTH = 1024
BLOCK_SIZE = 30
MAP_HEIGHT = 750
MAP_WIDTH = 1020

class ManagerEnv(object):
    def __init__(self, nb_drones, map_real_dims, map_simu_dims, start_pos, targets_pos, obstacles_pos) -> None:

        self.map_real_dims = map_real_dims
        self.map_simu_dims = map_simu_dims

        self.max_w = self.map_simu_dims[0]
        self.max_h = self.map_simu_dims[1]
    
        self.nb_drones = 1
        self.battery_actions = 1000
        self.drones = [Drone(start_pos) for i in range(nb_drones)]
        self.drone_pos = self.__coordinates_to_integers(self.drones[0].pos)
        self.launched_drones = []
        
        self.start_pos = self.__coordinates_to_integers(start_pos)
        self.targets_pos = [self.__coordinates_to_integers(targets_pos[0])]
        self.visited_targets = []
        
        self.obstacles_pos = obstacles_pos
        
        self.action_space = Discrete(len(Actions) * self.nb_drones,)
        self.mapping_actions = dict((item.value, item) for item in Actions)
        self.nb_states = self.max_w * self.max_h

        self.screen = None
        self.clock = None
        self.white = (255, 255, 255)

    def reset(self, seed=None, options=None):

        self.state = 0
        self.launched_drones = []
        # self.nb_drones = self.nb_drones
        # self.drones = [Drone(self.start_pos) for i in range(self.nb_drones)]
        self.drone_pos = self.start_pos
        self.visited_targets = []
        self.battery_actions = 1000

        return self.drone_pos

    def __out_of_bounds(self, pos):
        x, y = pos
        return (x < 0 or x > self.max_w or y < 0 or y > self.max_h)

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
        self.battery_actions -= 1

        reward = -1
        done = False

        if (not self.action_space.contains(action)):
            return

        # drone_id = action // len(Actions)
        drone_id = 0
        tmp_pos = self.drones[drone_id].pos

        if self.mapping_actions[action] == Actions.LAUNCH:
            if (not self.drones[drone_id].launched):
                self.drones[drone_id].launched = True
                reward = -10
                # PrintInDroneFile
                self.launched_drones.append(self.drones[drone_id])
            else:
                reward = -20

        elif self.mapping_actions[action] == Actions.FORWARD:
            if (self.drones[drone_id].launched):
                self.drones[drone_id].forward()
                # PrintInDroneFile
            else:
                reward = -20

        elif self.mapping_actions[action] == Actions.RIGHT:
            if (self.drones[drone_id].launched):
                self.drones[drone_id].right()
                # PrintInDroneFile
            else:
                reward = -20

        elif self.mapping_actions[action] == Actions.BACKWARDS:
            if (self.drones[drone_id].launched):
                self.drones[drone_id].backward()
                # PrintInDroneFile
            else:
                reward = -20

        elif self.mapping_actions[action] == Actions.LEFT:
            if (self.drones[drone_id].launched):
                self.drones[drone_id].left()
                # PrintInDroneFile
            else:
                reward = -20

        elif self.mapping_actions[action] == Actions.ROTATE_RIGHT:
            if (self.drones[drone_id].launched):
                self.drones[drone_id].rotate(1)
                # PrintInDroneFile
            else:
                reward = -20

        elif self.mapping_actions[action] == Actions.ROTATE_LEFT:
            if (self.drones[drone_id].launched):
                self.drones[drone_id].rotate(-1)
                # PrintInDroneFile
            else:
                reward = -20

        elif self.mapping_actions[action] == Actions.UP:
            if (self.drones[drone_id].launched):
                # PrintInDroneFile
                self.drones[drone_id].up()
            else:
                reward = -20

        elif self.mapping_actions[action] == Actions.DOWN:
            if (self.drones[drone_id].launched):
                # PrintInDroneFile
                self.drones[drone_id].down()
            else:
                reward = -20

        elif self.mapping_actions[action] == Actions.DO_TASK:
            if (self.drones[drone_id].launched):
                if (self.drone_pos == self.targets_pos[0] and self.targets_pos[0] not in self.visited_targets):
                    # PrintInDroneFile
                    reward = 50
                    self.visited_targets.append(self.targets_pos[0])
                else:
                    reward = -10
            else:
                reward = -20

        elif self.mapping_actions[action] == Actions.LAND:
            if (self.drones[drone_id] in self.launched_drones):
                self.launched_drones.remove(self.drones[drone_id])
                # PrintInDroneFile
            else:
                reward = -50

        if (self.__out_of_bounds(self.drones[drone_id].pos)):  # """or self.drones[drone_id].pos in [(p[0],p[1]) for p in self.obstacles_pos]"""):
            self.drones[drone_id].pos = tmp_pos
            done = True
            reward = -1000

        # elif (self.drones[drone_id].battery <= 0):
        #   #print("Battery done")
        #   reward = -100
        #   done = True

        if self.targets_pos[0] in self.visited_targets and self.drone_pos == self.start_pos:
            # Targets done
            done = True
            reward = 100

        if (self.battery_actions <= 0):
            # Battery outOfOrder
            reward = -100
            done = True

        self.drone_pos = self.__coordinates_to_integers(self.drones[drone_id].pos)
        return (self.drone_pos, reward, done, False, {})


    def __draw_grid(self):
        black = (0, 0, 0)
        for x in range(0, MAP_WIDTH, BLOCK_SIZE):
            for y in range(0, MAP_HEIGHT, BLOCK_SIZE):
                rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, black, rect, 1)

    def __draw_obstacle(self, obstacle_pos):

        font_simu = pygame.font.SysFont('liberationmono', BLOCK_SIZE, True)
        black = (0, 0, 0)
        alt_color = (255, 195, 0)
        for i in range(0, BLOCK_SIZE):
            for j in range(0, BLOCK_SIZE):
                if ((i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0)):
                    rect = pygame.Rect(
                        obstacle_pos[0] * BLOCK_SIZE + j, obstacle_pos[1] * BLOCK_SIZE + i, 1, 1)
                    pygame.draw.rect(self.screen, black, rect, 1)
        if (int(obstacle_pos[2]) > 0 and font_simu != None):
            text_obstacle = font_simu.render(
                str(obstacle_pos[2]), True, alt_color)
            self.screen.blit(
                text_obstacle, (obstacle_pos[0] * BLOCK_SIZE, obstacle_pos[1] * BLOCK_SIZE))

    def __draw_target(self):
        target_col = (0, 255, 0)
        if (not self.targets_pos[0] in self.visited_targets):
            target_pos = self.__integers_to_coordinates(self.targets_pos[0])
            pygame.draw.circle(self.screen, target_col, (target_pos[0] * BLOCK_SIZE + (
                BLOCK_SIZE - 1)/2, target_pos[1] * BLOCK_SIZE + (BLOCK_SIZE - 1)/2), BLOCK_SIZE/2, 5)

    def __draw_house(self):
        col_wall = (255, 228, 225)
        col_door = (165, 42, 42)
        col_roof = (255, 0, 0)

        start = self.__integers_to_coordinates(self.start_pos)
        wall = pygame.Rect(start[0] * BLOCK_SIZE + (1/5) * BLOCK_SIZE,
                           start[1] * BLOCK_SIZE + (2/3) * BLOCK_SIZE, 20, 10)
        door = pygame.Rect(start[0] * BLOCK_SIZE + (1/2) * BLOCK_SIZE,
                           start[1] * BLOCK_SIZE + (5/6) * BLOCK_SIZE, 2, 5)

        start_roof = (start[0] * BLOCK_SIZE + (1/2) *
                      BLOCK_SIZE, start[1] * BLOCK_SIZE)
        roof_b = (start[0] * BLOCK_SIZE + BLOCK_SIZE,
                  start[1] * BLOCK_SIZE + (2/3) * BLOCK_SIZE)
        roof_c = (start[0] * BLOCK_SIZE, start[1] *
                  BLOCK_SIZE + (2/3) * BLOCK_SIZE)

        pygame.draw.polygon(self.screen, col_roof,
                            (start_roof, roof_b, roof_c))
        pygame.draw.rect(self.screen, col_wall, wall)
        pygame.draw.rect(self.screen, col_door, door)

    def render(self):

        if self.screen is None:
            pygame.init()
            pygame.display.init()
            self.screen = pygame.display.set_mode(
                (WINDOW_WIDTH, WINDOW_HEIGHT))
        if self.clock is None:
            self.clock = pygame.time.Clock()

        self.screen.fill(self.white)
        self.__draw_grid()
        self.__draw_house()

        for i in range(len(self.obstacles_pos)):
            self.__draw_obstacle(self.obstacles_pos[i])
        # for i in range(len(self.targets_pos)):
        #   self.__draw_target(self.targets_pos[i])
        # for i in range(len(self.drones)):
        #   self.drones[i].draw_drone(screen, BLOCK_SIZE)

        self.__draw_target()
        self.drones[0].draw_drone(self.screen, BLOCK_SIZE)

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

        self.clock.tick(6)
