import pygame, sys, random
from pygame.locals import*

WINDW = 640
WINDH = 480
NUMCOLS = 4
NUMROWS = 4
TILESIZE = 80
TILEGAP = 2
SCRAMBLELENGTH = 20
FPS = 30
SLIDESPEED = 0.1 # slide time in seconds
BLANK = None
XMARGIN = int((WINDW - NUMCOLS*(TILESIZE + TILEGAP)) / 2)
YMARGIN = int((WINDH - NUMROWS*(TILESIZE + TILEGAP)) / 2)
BOTTOMXMARGIN = 20
BOTTOMYMARGIN = 20

BLACK         = (  0,   0,   0)
WHITE         = (255, 255, 255)
BRIGHTBLUE    = (  0,  50, 255)
DARKTURQUOISE = (  3,  54,  73)
GREEN         = (  0, 204,   0)

BGCOLOR = DARKTURQUOISE
BGFLASHCOLOR = BRIGHTBLUE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONT = 'freesansbold.ttf'
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

def main():
    pygame.init()

    clock = pygame.time.Clock()
    display = pygame.display.set_mode((WINDW, WINDH))
    pygame.display.set_caption('Sliding Puzzle')

    # init variables
    board = getStartingBoard()
    drawBoard(display, board, BGCOLOR)
    newGameRect, solveRect = drawButtons(display)
    pygame.display.update()

    # scramble
    seq = animateStart(display, clock, board)
    
    # main loop
    while True:
        checkForQuit()
        if hasWon(board):
            for i in range(10):
                flashScreen(display, clock, board)
            pygame.time.wait(250) # short pause
            seq = animateStart(display, clock, board)

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                tileX, tileY = getTileAtPixel(event.pos[0], event.pos[1])
                if tileX != None and tileY != None:
                    moveTileAt(display, clock, board, tileX, tileY, seq)
                else: # not clicked on a tile, check for button click
                    if newGameRect.collidepoint(event.pos[0], event.pos[1]):
                        # reset
                        board = getStartingBoard()
                        drawBoard(display, board, BGCOLOR)
                        newGameRect, solveRect = drawButtons(display)
                        
                        pygame.display.update()
                        pygame.time.wait(250) # short pause
                        seq = animateStart(display, clock, board)
                    elif solveRect.collidepoint(event.pos[0], event.pos[1]):
                        sol = [getOpposite(step) for step in reversed(seq)]
                        makeMoves(display, clock, board, sol)


##### GAME FUNCTIONS #####

def flashScreen(surface, clock, board):
    drawBoard(surface, board, BGFLASHCOLOR)
    drawButtons(surface)
    pygame.display.update()
    pygame.time.wait(100)
    
    drawBoard(surface, board, BGCOLOR)
    drawButtons(surface)
    pygame.display.update()
    pygame.time.wait(100)

def makeMoves(surface, clock, board, seq):
    for step in seq:
        moveTileIn(surface, clock, board, step)

def moveTileAt(surface, clock, board, x, y, seq):
    ''' attempts to move (x, y) tile '''
    direction = getValidDirection(board, x, y)
    if direction != None:
        moveTileIn(surface, clock, board, direction)
        seq.append(direction)

def moveTileIn(surface, clock, board, direction):
    ''' move tile in specified direction '''
    blank = getBlank(board)
    src = getNeighbor(blank, getOpposite(direction))
    if src != None and isOnBoard(src[0], src[1]):
        # animate
        animateSlide(surface, clock, board, direction)
        # update board
        board[blank[0]][blank[1]], board[src[0]][src[1]] = board[src[0]][src[1]], board[blank[0]][blank[1]]

        
##### ANIMATE #####

def animateStart(surface, clock, board):
    ''' scrambling animation '''
    count = 0
    lastMove = None
    seq = []
    while count < SCRAMBLELENGTH:
        randDir = random.choice(DIRECTIONS)
        if randDir == getOpposite(lastMove): # undo-ing last move
            continue
        elif isValidDirection(board, randDir):
            moveTileIn(surface, clock, board, randDir)
            lastMove = randDir
            count += 1
            seq.append(randDir)
    return seq

def animateSlide(surface, clock, board, direction):
    ''' animate the movement of tile at src to dest '''
    # find the tile that needs to slide
    blank = getBlank(board)
    src = getNeighbor(blank, getOpposite(direction))
    steps = int( SLIDESPEED * FPS )
    inc = 1 / steps * (TILESIZE + TILEGAP)
    pX, pY = getTopLeftOfTileAt(src[0], src[1])
    dX, dY = getVector(direction)
    num = board[src[0]][src[1]]
    
    for i in range(steps):
        # draw over old tile
        drawBlankTileAtPixel(surface, int(round(pX)), int(round(pY)))
        # draw new tile
        pX += inc * dX
        pY += inc * dY
        drawNumberTileAtPixel(surface, int(round(pX)), int(round(pY)), num)
        pygame.display.update()
        clock.tick(FPS)    

    
##### DRAWING #####

def drawBoard(surface, board, color):
    surface.fill(color)
    drawTiles(surface, board)
    drawBorder()

def drawButtons(surface):
    newGameLabel = 'NEW GAME'
    solveLabel   = ' SOLVE  '
    # new game
    newGameText = getText(newGameLabel, BASICFONT, BASICFONTSIZE, TEXTCOLOR, TILECOLOR)
    newGameRect = newGameText.get_rect()
    newGameRect.bottomright = (WINDW - BOTTOMXMARGIN, WINDH - BOTTOMYMARGIN - BASICFONTSIZE - TILEGAP)
    surface.blit(newGameText, newGameRect)

    solveText = getText(solveLabel, BASICFONT, BASICFONTSIZE, TEXTCOLOR, TILECOLOR)
    solveRect = solveText.get_rect()
    solveRect.center = (newGameRect.center[0], newGameRect.center[1] + BASICFONTSIZE + TILEGAP)
    surface.blit(solveText, solveRect)

    return newGameRect, solveRect

def drawBorder():
    pass

def drawTiles(surface, board):
    for c in range(NUMCOLS):
        for r in range(NUMROWS):
            drawTileAtCR(surface, board, c, r)

def drawTileAtCR(surface, board, c, r):
    pX, pY = getTopLeftOfTileAt(c, r)
    num = board[c][r]
    if num:
        drawNumberTileAtPixel(surface, pX, pY, num)
    else:
        drawBlankTileAtPixel(surface, pX, pY)

def drawNumberTileAtPixel(surface, pX, pY, number):
    pygame.draw.rect(surface, TILECOLOR, (pX, pY, TILESIZE, TILESIZE))
    text = getText(str(number), BASICFONT, BASICFONTSIZE, TEXTCOLOR, TILECOLOR)
    textRect = text.get_rect() # correctly sized rect
    textRect.center = ( pX + int(TILESIZE / 2), pY + int(TILESIZE / 2) )
    surface.blit(text, textRect)

def drawBlankTileAtPixel(surface, pX, pY):
    pygame.draw.rect(surface, BGCOLOR, (pX, pY, TILESIZE, TILESIZE))


##### HELPER FUNCTIONS #####

def hasWon(board):
    return board == getStartingBoard()

def getValidDirection(board, x, y):
    blank = getBlank(board)
    for direction in DIRECTIONS:
        n = getNeighbor((x, y), direction)
        # check if n is the blank
        if n != None and n[0] == blank[0] and n[1] == blank[1]:
            return direction
    return None

def isValidDirection(board, direction):
    blank = getBlank(board)
    src = getNeighbor(blank, getOpposite(direction))
    return src != None and isOnBoard(src[0], src[1])

def isOnBoard(x, y):
    return (0 <= x and x < NUMCOLS) and (0 <= y and y < NUMROWS)

def getText(msg, font, fontsize, textColor, BGColor):
    ''' returns the text surface object '''
    font = pygame.font.Font(font, fontsize)
    text = font.render(msg, True, textColor, BGColor)
    return text

def getBlank(board):
    ''' returns the (x, y) of the BLANK entry in board '''
    for c in range(NUMCOLS):
        for r in range(NUMROWS):
            if board[c][r] == BLANK:
                return (c, r)

def getTopLeftOfTileAt(c, r):
    pX = c * (TILESIZE + TILEGAP) + XMARGIN
    pY = r * (TILESIZE + TILEGAP) + YMARGIN
    return (pX, pY)

def getTileAtPixel(pX, pY):
    for c in range(NUMCOLS):
        for r in range(NUMROWS):
            # get region
            x, y = getTopLeftOfTileAt(c, r)
            rect = pygame.Rect(x, y, TILESIZE, TILESIZE)
            # test collision
            if rect.collidepoint((pX, pY)):
                return (c, r)
    return (None, None)

def getNeighbor(src, direction):
    ''' get the cell in the direction '''
    # return None if no such neigbor
    dX, dY = getVector(direction)
    x = src[0] + dX
    y = src[1] + dY
    if isOnBoard(x, y):
        return (x, y)

def getOpposite(direction):
    if direction == UP:
        return DOWN
    elif direction == DOWN:
        return UP
    elif direction == LEFT:
        return RIGHT
    elif direction == RIGHT:
        return LEFT
    else:
        return None
    
def getVector(direction):
    if direction == UP:
        return 0, -1
    elif direction == DOWN:
        return 0, 1
    elif direction == LEFT:
        return -1, 0
    elif direction == RIGHT:
        return 1, 0
    else:
        return None, None

def getStartingBoard():
    board = [list(range(x, NUMROWS * NUMCOLS, NUMCOLS)) for x in range(NUMCOLS)]
    board[0][0] = None
    return board

def checkForQuit():
    for event in pygame.event.get(QUIT):
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)

def terminate():
    pygame.quit()
    sys.exit()



# call main
if __name__ == '__main__':
    main()





