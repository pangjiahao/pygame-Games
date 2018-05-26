import pygame, sys, random
from pygame.locals import *

# constants
FPS = 30
WINDW = 640
WINDH = 480
REVEALSPD = 8
BOXSIZE = 40
GAPSIZE = 10
NUMCOLS = 6
NUMROWS = 5
XMARGIN = int(WINDW - (NUMCOLS * (BOXSIZE + GAPSIZE))) / 2
YMARGIN = int(WINDH - (NUMROWS * (BOXSIZE + GAPSIZE))) / 2
PREVIEWTIME = 3
WRONGPAIRVIEWTIME = 0.75
FONTSIZE = 40

assert (NUMCOLS * NUMROWS) % 2 == 0, 'Number of cells must be even'
assert XMARGIN > 0, 'Too many cols'
assert YMARGIN > 0, 'Too many rows'

# colors
GRAY      = (100, 100, 100)
NAVYBLUE  = ( 60,  60, 100)
WHITE     = (255, 255, 255)
RED       = (255,   0,   0)
GREEN     = (  0, 255,   0)
BLUE      = (  0,   0, 255)
YELLOW    = (255, 255,   0)
ORANGE    = (255, 128,   0)
PURPLE    = (255,   0, 255)
CYAN      = (  0, 255, 255)
BLACK     = (  0,   0,   0)

BBGCOLOR = BLACK
BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = RED

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
CROSS = 'cross'
CIRCLE = 'circle'

OPEN = 'open'
CLOSE = 'close'

COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
SHAPES = (DONUT, SQUARE, DIAMOND, CROSS, CIRCLE)
assert len(COLORS) * len(SHAPES) * 2 >= NUMCOLS * NUMROWS, 'Number of cells is too large'

def main():
    pygame.init()

    # init screen and clock
    display = pygame.display.set_mode((WINDW, WINDH))
    pygame.display.set_caption('Memory Game')
    clock = pygame.time.Clock()

    # init data struct
    mouseX, mouseY = 0, 0
    board = getBoard()
    covered = getCovers()
    firstSelection = None # used for tracking 1st or 2nd click
    numMoves = 0

    animateGameStart(display, clock, board)

    # main game loop
    while True:
        # draw board
        display.fill(BBGCOLOR)
        drawBoard(display, board, covered)
        drawCount(display, numMoves)
        
        # reset vars
        mouseClicked = False

        # get input
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouseX, mouseY = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouseX, mouseY = event.pos
                mouseClicked = True

        # process input
        boxX, boxY = getBoxAtPixels(mouseX, mouseY)
        if boxX != None and boxY != None:
            # highlight hovered box if it is covered
            if covered[boxX][boxY]:
                drawHighlight(display, boxX, boxY)
            if covered[boxX][boxY] and mouseClicked: # box has been clicked
                numMoves += 1
                covered[boxX][boxY] = False
                icon = board[boxX][boxY]
                animateBoxes(display, clock, board, [(boxX, boxY)], OPEN)

                # check if this is first or second box
                if firstSelection == None:
                    firstSelection = (boxX, boxY)
                else: # check if game won, successful match, or fail
                    if isWon(covered):
                        animateWin(display, numMoves)
                        
                        # reset
                        board = getBoard()
                        covered = getCovers()
                        firstSelection = None
                        numMoves = 0

                        animateGameStart(display, clock, board)
                    elif isMatch(board, firstSelection, (boxX, boxY)):
                        firstSelection = None
                    else: # pause, then close both
                        pygame.time.wait(int( WRONGPAIRVIEWTIME * 1000 ))
                        covered[boxX][boxY] = True
                        covered[firstSelection[0]][firstSelection[1]] = True
                        boxes = [(boxX, boxY), (firstSelection[0], firstSelection[1])]
                        animateBoxes(display, clock, board, boxes, CLOSE)
                        firstSelection = None
                        
        drawCount(display, numMoves)
        pygame.display.update()
        clock.tick(FPS)


##### animation functions #####

def animateGameStart(surface, clock, board):
    boxes = [(x, y) for x in range(NUMCOLS) for y in range(NUMROWS)]
    covered = getCovers()

    # show covered board
    surface.fill(BBGCOLOR)
    drawBoard(surface, board, covered)
    drawCount(surface, 0)
    pygame.display.update()
    pygame.time.wait(100)

    # uncover board for a while
    animateBoxes(surface, clock, board, boxes, OPEN)
    pygame.time.wait(PREVIEWTIME * 1000)
    animateBoxes(surface, clock, board, boxes, CLOSE)

def animateWin(surface, numMoves):
    drawCount(surface, numMoves, False)
    fontObj = pygame.font.Font('freesansbold.ttf', 40)
    textSurfaceObj = fontObj.render('WINNER! MOVES: {}'.format(numMoves), True, RED, BBGCOLOR)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (int(WINDW / 2), 50)

    surface.blit(textSurfaceObj, textRectObj)
    pygame.display.update()
    pygame.time.wait(3000)

def animateBoxes(surface, clock, board, boxes, way):
    steps = int( BOXSIZE / REVEALSPD )

    # open or close
    if way == OPEN:
        r = range(steps, -1, -1)
    elif way == CLOSE:
        r = range(steps)

    for i in r:
        percentage = i/steps
        for box in boxes:
            boxX, boxY = box
            drawCell(surface, board[boxX][boxY], boxX, boxY, percentage)
        
        pygame.display.update()
        clock.tick(FPS)


##### drawing functions #####

def drawCount(surface, num, flag=True):
    color = (RED if flag else BBGCOLOR)
    
    fontObj = pygame.font.Font('freesansbold.ttf', FONTSIZE)
    textSurfaceObj = fontObj.render('COUNT: {}'.format(str(num)), True, color, BBGCOLOR)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.topleft = (0, 0)
    surface.blit(textSurfaceObj, textRectObj)

def drawBoard(surface, board, covered):
    for boxX in range(NUMCOLS):
        for boxY in range(NUMROWS):
            icon = board[boxX][boxY]
            percentage = 1 if covered[boxX][boxY] else 0
            drawCell(surface, icon, boxX, boxY, percentage)

def drawCell(surface, icon, boxX, boxY, percentage):
    """ draw the whole cell properly """
    # draw BG, draw icon, draw cover
    drawCover(surface, BGCOLOR, boxX, boxY, 1)
    drawIcon(surface, icon, boxX, boxY)
    if percentage > 0:
        drawCover(surface, BOXCOLOR, boxX, boxY, percentage)

def drawIcon(surface, icon, boxX, boxY):
    """ icon is a tuple of (shape color) """
    shape = icon[0]
    color = icon[1]

    x, y = getTopLeftCoords(boxX, boxY)
    half = int(BOXSIZE / 2)
    tenth = int(BOXSIZE / 10)
    centerX = x + half
    centerY = y + half
    
    if shape == DONUT:
        pygame.draw.circle(surface, color, (centerX, centerY), 3*tenth, 2*tenth)
    elif shape == CIRCLE:
        pygame.draw.circle(surface, color, (centerX, centerY), 3*tenth)
    elif shape == SQUARE:
        pygame.draw.rect(surface, color, (x + 2*tenth, y + 2*tenth, 6*tenth, 6*tenth))
    elif shape == DIAMOND:
        pygame.draw.polygon(surface, color, ((x + half, y), (x + BOXSIZE - 1, y + half), (x + half, y + BOXSIZE - 1), (x, y + half)))
    elif shape == CROSS:
        pygame.draw.rect(surface, color, (x + 4*tenth, y + tenth, 2*tenth, 8*tenth))
        pygame.draw.rect(surface, color, (x + tenth, y + 4*tenth, 8*tenth, 2*tenth))

def drawCover(surface, color, boxX, boxY, percentage):
    """ draw a partial cover at location of box """
    x, y = getTopLeftCoords(boxX, boxY)
    pygame.draw.rect(surface, color, (x, y, int(BOXSIZE*percentage), BOXSIZE))

def drawHighlight(surface, boxX, boxY):
    x, y = getTopLeftCoords(boxX, boxY)
    border = int( GAPSIZE / 2 )
    pygame.draw.rect(surface, HIGHLIGHTCOLOR, (x - border, y - border, BOXSIZE + 2*border, BOXSIZE + 2*border), border - 1)
    

##### helper functions #####
    
def isWon(covered):
    for col in covered:
        if True in col:
            return False
    return True
                
def isMatch(board, p1, p2):
    """ check if the icons at p1 and p2 are a match """
    icon1 = board[p1[0]][p1[1]]
    icon2 = board[p2[0]][p2[1]]
    return icon1[0] == icon2[0] and icon1[1] == icon2[1]

def getBoard():
    """ returns a 2D matrix filled with icons """
    icons = [(shape, color) for shape in SHAPES for color in COLORS]
    numIconsNeeded = int( (NUMROWS * NUMCOLS) / 2 )
    
    random.shuffle(icons)
    icons = icons[:numIconsNeeded] * 2
    random.shuffle(icons)

    board = [icons[i:i + NUMROWS] for i in range(0, NUMCOLS * NUMROWS, NUMROWS)]
    return board

def getCovers():
    return [([True] * NUMROWS) for c in range(NUMCOLS)]

def getTopLeftCoords(boxX, boxY):
    """ given a box, return the pixel coords of its top left corner """
    x = int( boxX * (BOXSIZE + GAPSIZE) + XMARGIN )
    y = int( boxY * (BOXSIZE + GAPSIZE) + YMARGIN )
    return (x, y)

def getBoxAtPixels(pixelX, pixelY):
    """ try each box coord to see if any match with pixel X and Y """
    for boxX in range(NUMCOLS):
        for boxY in range(NUMROWS):
            # get the region of this box
            x, y = getTopLeftCoords(boxX, boxY)
            boxRect = pygame.Rect(x, y, BOXSIZE, BOXSIZE)
            # check collision
            if boxRect.collidepoint(pixelX, pixelY):
                return (boxX, boxY)
    return (None, None)


if __name__ == '__main__':
    main()











