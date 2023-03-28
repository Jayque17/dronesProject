import pygame

class Drone():
  def __init__(self, start_pos) -> None:
    self.launched = True
    self.battery = 20
    self.vect = 6
    self.altitude = 1
    self.rotations = [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
    self.pos = start_pos
    self.current_rot = self.rotations[self.vect]

  def rotate(self, dir):
    self.vect = (self.vect + dir) % 8
    self.battery -= 1
  
  def forward(self):
    self.pos = (self.pos[0] + self.rotations[self.vect][0],self.pos[1] + self.rotations[self.vect][1])
    #self.pos = self.pos + self.rotations[self.vect]
    self.battery -= 1

  def right(self):
    self.pos = (self.pos[0] + self.rotations[(self.vect + 2) % 8][0],self.pos[1] + self.rotations[(self.vect + 2) % 8][1])
    self.battery -= 1
    #self.pos = self.pos + self.rotations[(self.vect + 2) % 8]
    
  def backward(self):
    self.pos = (self.pos[0] + self.rotations[(self.vect + 4) % 8][0],self.pos[1] + self.rotations[(self.vect + 4) % 8][1])    
    self.battery -= 1
    #self.pos = self.pos + self.rotations[(self.vect + 4) % 8]
    
  def left(self):
    self.pos = (self.pos[0] + self.rotations[(self.vect + 6) % 8][0],self.pos[1] + self.rotations[(self.vect + 6) % 8][1])
    self.battery -= 1
    #self.pos = self.pos + self.rotations[(self.vect + 6) % 8]
    
  def up(self):
    self.altitude += 1
    self.battery -= 1
    
  def down(self):
    self.altitude -= 1
    self.battery -= 1
    

  def draw_drone(self, screen, block_size):
    self.current_rot = self.rotations[self.vect]
    radius = 10
    blue = (0, 0, 255)
    arrow_col = (199,21,133)

    x =  self.pos[0] * block_size + block_size/2
    y =  self.pos[1] * block_size + block_size/2
    circle = pygame.draw.circle(screen, blue, (x, y), radius)
    
    # Est
    if self.current_rot == self.rotations[0]:    
      start_arrow = (x + 5 + radius, y)
      arrow_b = (start_arrow[0] - 5, start_arrow[1] + 5)
      arrow_c = (start_arrow[0] - 5, start_arrow[1] - 5)   
    
    # SE
    elif self.current_rot == self.rotations[1]:    
      start_arrow = (x + radius, y + radius)
      arrow_b = (start_arrow[0] - 5, start_arrow[1])
      arrow_c = (start_arrow[0], start_arrow[1] - 5)
    
    # South
    elif self.current_rot == self.rotations[2]:    
      start_arrow = (x, y + 5 + radius)
      arrow_b = (start_arrow[0] - 5, start_arrow[1] - 5)
      arrow_c = (start_arrow[0] + 5, start_arrow[1] - 5)

    # SW
    elif self.current_rot == self.rotations[3]:
      start_arrow = (x - radius, y + radius)
      arrow_b = (start_arrow[0], start_arrow[1] - 5)
      arrow_c = (start_arrow[0] + 5, start_arrow[1])    
      
    # West
    elif self.current_rot == self.rotations[4]:    
      start_arrow = (x - (5 + radius), y)
      arrow_b = (start_arrow[0] + 5, start_arrow[1] + 5)
      arrow_c = (start_arrow[0] + 5, start_arrow[1] - 5)       
    
    # NW
    elif self.current_rot == self.rotations[5]:    
      start_arrow = (x - radius, y - radius)
      arrow_b = (start_arrow[0] + 5, start_arrow[1])
      arrow_c = (start_arrow[0], start_arrow[1] + 5)    
      
    # North
    elif self.current_rot == self.rotations[6]:    
      start_arrow = (x, y - (5 + radius))
      arrow_b = (start_arrow[0] + 5, start_arrow[1] + 5)
      arrow_c = (start_arrow[0] - 5, start_arrow[1] + 5)    
    
    # NE
    elif self.current_rot == self.rotations[7]:
      start_arrow = (x  + radius, y - radius)
      arrow_b = (start_arrow[0] - 5, start_arrow[1])
      arrow_c = (start_arrow[0], start_arrow[1] + 5)    
      
    else:    
      raise Exception("unhandle parameter")
    
    arrow = pygame.draw.polygon(screen, arrow_col, (start_arrow, arrow_b, arrow_c))
    

