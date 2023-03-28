
# import pygame
# import sys
# from time import sleep


WINDOW_HEIGHT = 800
WINDOW_WIDTH = 800


max_w = 20
max_h = 7
screen = None
clock = None
white = (255, 255, 255)
black = (0, 0, 0)
font_simu = None
block_size = WINDOW_WIDTH//2//max_w


# def draw_grid(self):
#     for x in range(0, WINDOW_WIDTH, self.block_size):
#         for y in range(0, WINDOW_HEIGHT//2, self.block_size):
#             rect = pygame.Rect(x, y, self.block_size, self.block_size)
#             pygame.draw.rect(self.screen, self.black, rect, 1)



# def render(Qtable=None):

#     if screen is None:
#         pygame.init()
#         pygame.display.init()
#         screen = pygame.display.set_mode(
#             (WINDOW_WIDTH, WINDOW_HEIGHT))
#     if clock is None:
#         clock = pygame.time.Clock()
#     if font_simu is None:
#         font_simu = pygame.font.SysFont('liberationmono', block_size, True)

#     screen.fill(white)
#     # if(Qtable == None):

#     # view = pygame.surfarray.array3d(screen)
#     # view = view.transpose([1, 0, 2])
#     # img_bgr = cv2.cvtColor(view, cv2.COLOR_RGB2BGR)
#     # cv2.imshow(img_bgr)
#     # time.sleep(wait_time)

#     # canvas = pygame.Surface((window_size, window_size))
#     # canvas.fill((255, 255, 255))
#     # window.blit(canvas, canvas.get_rect())

#     #pygame.event.pump()
#     pygame.display.update()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     clock.tick(0.8)


# if __name__ == "__main__":


#     if screen is None:
#         pygame.init()
#         pygame.display.init()
#         screen = pygame.display.set_mode(
#             (WINDOW_WIDTH, WINDOW_HEIGHT))
#     if clock is None:
#         clock = pygame.time.Clock()
#     if font_simu is None:
#         font_simu = pygame.font.SysFont('liberationmono', block_size, True)

#     screen.fill(white)

#     pygame.display.update()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()
#     clock.tick(0.8)

#     for x in range(0, WINDOW_WIDTH, block_size):
#         for y in range(0, WINDOW_HEIGHT//2, block_size):
#             rect = pygame.Rect(x, y, block_size, block_size)
#             pygame.draw.rect(screen, black, rect, 1)

    
#     sleep(100)


import pygame
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()
 
# Set the width and height of the screen [width, height]
size = (700, 500)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

arrow = pygame.Surface((350, 350), pygame.SRCALPHA, 32)


pygame.draw.polygon(arrow, (0, 0, 0), ((25, 125), (25, 225), (225, 225), (225, 325), (325, 175), (225, 25), (225, 125)))
scaled_arrow = pygame.transform.scale(arrow, (block_size, block_size))

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
    # --- Game logic should go here
 
    # --- Screen-clearing code goes here
 
    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
 
    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(WHITE)
 
    #screen.blit(arrow, (0, 0))
    

    # --- Drawing code should go here
    i = 0
    for x in range(0, WINDOW_WIDTH, block_size):
        for y in range(0, WINDOW_HEIGHT//2, block_size):
            rect = pygame.Rect(x, y, block_size, block_size)
            pygame.draw.rect(screen, black, rect, 1)
            i+=1
            screen.blit(pygame.transform.rotate(scaled_arrow, 90. * (i%4)), (x, y))
    
    


    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()




