'''
Simulate Game
made with reference to 'Making Games with Python and Pygame' by Al Sweigart
'''

import pygame, sys, random, time
from mycolors import *
from pygame.locals import *

WINDW = 700
WINDH = 500
BUTTONSIZE = 200
BUTTONGAPSIZE = 20
MSGBOXW = 400
MSGBOXH = 50
MSGBOXXMARGIN = int( (WINDW - MSGBOXW) / 2 )
MSGBOXYMARGIN = 10
XMARGIN = int( (WINDW - 2*BUTTONSIZE - BUTTONGAPSIZE) / 2 )
YMARGIN = int( (WINDH - 2*BUTTONSIZE - BUTTONGAPSIZE) * 3 / 4 )

FONT = 'freesansbold.ttf'
FONTSIZE = 24
FONTCOLOR = WHITE

FPS = 40
FLASHSPEED = 500 # in ms
FLASHDELAY = 200 # in ms
TIMEOUT = 4

BGCOLOR = BLACK
YELLOWBTN = 'yellow'
BLUEBTN = 'blue'
REDBTN = 'red'
GREENBTN = 'green'
BUTTONS = [YELLOWBTN, BLUEBTN, REDBTN, GREENBTN]

def main():
    # init
    pygame.init()
    display = pygame.display.set_mode((WINDW, WINDH))
    pygame.display.set_caption('Simulate')
    clock = pygame.time.Clock()
    # get rects for drawing. doable since small amount
    yellowRect = pygame.Rect(XMARGIN, YMARGIN, BUTTONSIZE, BUTTONSIZE)
    blueRect = pygame.Rect(XMARGIN + BUTTONSIZE + BUTTONGAPSIZE, YMARGIN, BUTTONSIZE, BUTTONSIZE)
    redRect = pygame.Rect(XMARGIN, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE, BUTTONSIZE, BUTTONSIZE)
    greenRect = pygame.Rect(XMARGIN+ BUTTONSIZE + BUTTONGAPSIZE, YMARGIN + BUTTONSIZE + BUTTONGAPSIZE , BUTTONSIZE, BUTTONSIZE)
    msgBoxRect = pygame.Rect(MSGBOXXMARGIN, MSGBOXYMARGIN, MSGBOXW, MSGBOXH)
    buttons = ((YELLOWBTN, yellowRect), (BLUEBTN, blueRect), (REDBTN, redRect), (GREENBTN, greenRect))
    # draw initial screen
    display.fill(BGCOLOR)
    drawButtons(display, buttons)
    drawMsg(display, 'Try to remember the order', msgBoxRect)
    pygame.time.wait(1000)
    # variables
    seq = []
    waitingForPlayer = False
    clickedButton = None
    
    while True:
        if not waitingForPlayer:
            for i in range(3, 0, -1):
                drawMsg(display, 'Starting in {}'.format(i), msgBoxRect)
                pygame.time.wait(500)
            drawMsg(display, '', msgBoxRect)
            rand = random.choice(buttons)
            seq.append(rand)
            playSeq(display, clock, seq, msgBoxRect)
            playerSeq = seq[:]
            waitingForPlayer = True

        # read the input
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mX, mY = event.pos
                clickedButton = getClickedButton(mX, mY, buttons)
        
        # process player selection
        if clickedButton != None:
            animateClick(display, clock, clickedButton, msgBoxRect)

            if isCorrect(clickedButton, playerSeq):
                playerSeq = playerSeq[1:] # remove first elem

                if playerSeq == []: # player has input all correctly
                    waitingForPlayer = False
            else:
                # game over
                drawMsg(display, 'GAME OVER!', msgBoxRect)
                pygame.time.wait(2000)
                drawMsg(display, 'Final Score: {}'.format(len(seq) - 1), msgBoxRect)
                pygame.time.wait(3000)
                drawMsg(display, 'Starting New Game', msgBoxRect)
                pygame.time.wait(2000)
                drawMsg(display, '', msgBoxRect)
                
                seq = []
                waitingForPlayer = False

        clickedButton = None


##### GAME LEVEL #####





##### ANIMATION #####

def playSeq(surface, clock, seq, msgBoxRect):
    for button in seq:
        animateClick(surface, clock, button, msgBoxRect)

def animateClick(surface, clock, clickedButton, msgBoxRect, animationSpeed=30): # time in ms of animation
    if clickedButton[0] == YELLOWBTN:
        msg = 'YELLOW'
        rect = clickedButton[1]
        color = YELLOW
        flashColor = BRIGHTYELLOW
    elif clickedButton[0] == BLUEBTN:
        msg = 'BLUE'
        rect = clickedButton[1]
        color = BLUE
        flashColor = BRIGHTBLUE
    elif clickedButton[0] == REDBTN:
        msg = 'RED'
        rect = clickedButton[1]
        color = RED
        flashColor = BRIGHTRED
    elif clickedButton[0] == GREENBTN:
        msg = 'GREEN'
        rect = clickedButton[1]
        color = GREEN
        flashColor = BRIGHTGREEN

    # display the word also
    drawMsg(surface, msg, msgBoxRect)
    # use 2 button-sized surfaces to animate
    buttonSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    buttonSurf.fill(color)
    flashSurf = pygame.Surface((BUTTONSIZE, BUTTONSIZE))
    flashSurf = flashSurf.convert_alpha()

    r, g, b = flashColor
    for start, end, step in ((0, 255, 1), (255, 0, -1)):
        for alpha in range(start, end, animationSpeed * step):
            flashSurf.fill((r, g, b, alpha))
            surface.blit(buttonSurf, rect.topleft)
            surface.blit(flashSurf, rect.topleft)
            pygame.display.update()
            clock.tick(FPS)
    surface.blit(buttonSurf, rect.topleft)
    drawMsg(surface, '', msgBoxRect)
    pygame.display.update()
            

##### DRAWING #####
    
def drawButtons(surface, buttonList):
    for buttonName, buttonRect in buttonList:
        pygame.draw.rect(surface, getColorFromButton(buttonName), buttonRect)

def drawMsg(surface, msg, msgBoxRect):
    font = pygame.font.Font(FONT, FONTSIZE)
    text = font.render(msg, True, FONTCOLOR, BGCOLOR)
    rect = text.get_rect()
    rect.center = msgBoxRect.center
    pygame.draw.rect(surface, BGCOLOR, msgBoxRect)
    surface.blit(text, rect)
    pygame.display.update()

##### HELPER #####

def getColorFromButton(button):
    if button == YELLOWBTN:
        return YELLOW
    elif button == BLUEBTN:
        return BLUE
    elif button == REDBTN:
        return RED
    elif button == GREENBTN:
        return GREEN

def isCorrect(clickedButton, playerSeq):
    return clickedButton == playerSeq[0]

def getClickedButton(pX, pY, buttons):
    for button in buttons:
        if button[1].collidepoint(pX, pY):
            return button
    return None



if __name__ == '__main__':
    main()

