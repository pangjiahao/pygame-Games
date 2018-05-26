import pygame, sys
from pygame.locals import *

pygame.init()

class MovingRect: # rect, but with direction and speed
    def __init__(self, windW, windH, rect, horSpd, verSpd):
        self.rect = rect
        self.windW = windW
        self.windH = windH
        self.horD = 'R'
        self.verD = 'D'
        self.horSpd = horSpd
        self.verSpd = verSpd

    def move(self):
        # horizontally
        if self.horD == 'L':
            self.rect.left -= self.horSpd
            if self.rect.left <= 0:
                self.horD = 'R'
        else:
            self.rect.left += self.horSpd
            if self.rect.right >= self.windW:
                self.horD = 'L'
        #ver
        if self.verD == 'U':
            self.rect.top -= self.verSpd
            if self.rect.top <= 0:
                self.verD = 'D'
        else:
            self.rect.top += self.verSpd
            if self.rect.bottom >= self.windH:
                self.verD = 'U'

# variables
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
WINDW = 400
WINDH = 300
BOXW = 50

# set up
# clock
FPS = 40
clock = pygame.time.Clock()

# window
display = pygame.display.set_mode((WINDW, WINDH)) # depth = 0
pygame.display.set_caption('Moving Box')

# create box
mRect1 = pygame.Rect(0, 150, BOXW, BOXW)
mRect2 = pygame.Rect(150, 50, 2*BOXW, 0.5*BOXW)
movingRect1 = MovingRect(WINDW, WINDH, mRect1, 10, 5)
movingRect2 = MovingRect(WINDW, WINDH, mRect2, 5, 10)

while True:
    movingRect1.move()
    movingRect2.move()
    
    # draw
    display.fill(BLACK)
    pygame.draw.rect(display, WHITE, movingRect1.rect)
    pygame.draw.rect(display, WHITE, movingRect2.rect)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(FPS)




            
