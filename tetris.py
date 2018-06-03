# tetris
# made with reference to
# Making Games with Python & Pygame by Al Sweigart

import pygame, random, time, sys, mycolors
from pygame.locals import *

# DIMENSIONS
FPS = 60
WINDW = 640
WINDH = 480
CELLSIZE = 20
CELLBORDER = 2
GHOSTBORDER = 4
NUMCOLS = 10
NUMROWS = 20
BOTTOMMARGIN = 5
XMARGIN = int( (WINDW - NUMCOLS * CELLSIZE) / 2 )
YMARGIN = WINDH - NUMROWS * CELLSIZE - BOTTOMMARGIN
MAXSHIFTSIDEWAYS = NUMCOLS + 1
MAXSHIFTDOWNWARDS = NUMROWS + 2
STARTCOORDS = (NUMCOLS // 2, -1) # location of pieces when enter game
# previews
NUMPREVIEWS = 3
PREVIEWBOXSIZE = 5 * CELLSIZE
PREVIEWGAPSIZE = CELLSIZE
PREVIEWXMARGIN = XMARGIN + (NUMCOLS * CELLSIZE) + PREVIEWGAPSIZE
PREVIEWYMARGIN = YMARGIN
PREVIEWINITIALGRIDCOORDS = (NUMCOLS + 1 + 2, 2) # location of top preview
PREVIEWGRIDCOORDYOFFSET = 6 # magic num
PREVIEWRECTPIXELCOORDS = [(PREVIEWXMARGIN, PREVIEWYMARGIN + (i * (PREVIEWBOXSIZE + PREVIEWGAPSIZE))) for i in range(NUMPREVIEWS)]
PREVIEWGRIDCOORDS = [(PREVIEWINITIALGRIDCOORDS[0], PREVIEWINITIALGRIDCOORDS[1] + i*PREVIEWGRIDCOORDYOFFSET)for i in range(NUMPREVIEWS)]
# swap
SWAPRECTXMARGIN = XMARGIN - 6 * CELLSIZE
SWAPRECTYMARGIN = YMARGIN
SWAPBOXSIZE = 5 * CELLSIZE
SWAPGRIDCOORDS = (-4, 2)
TEXTBOXXMARGIN = XMARGIN - 9 * CELLSIZE
TEXTBOXYMARGIN = SWAPRECTYMARGIN + SWAPBOXSIZE + CELLSIZE
TEXTBOXW = 8 * CELLSIZE
TEXTBOXH = 4 * CELLSIZE
TEXTBOXRECT = pygame.Rect(TEXTBOXXMARGIN, TEXTBOXYMARGIN, TEXTBOXW, TEXTBOXH)
# controls
SOFTDROP = K_DOWN
HARDDROP = K_UP
ROTCW = K_c
ROTACW = K_z
ROTONE80 = K_x
SHIFTLEFT = K_LEFT
SHIFTRIGHT = K_RIGHT
SWAP = K_SPACE
NUMLINES = 40
# game settings
FLUSHDELAY = 0.2
SOFTDROPDELAY = 0.05
GRAVITYDELAY = 0.5
# colors
BGCOLOR = mycolors.BRIGHTBLUE
TEXTSCREENCOLOR = mycolors.BLACK
GRIDCOLOR = mycolors.BLACK
PIECECOLOR = mycolors.BRIGHTGREEN
PIECECOLORLIGHT = mycolors.VERYBRIGHTGREEN
PIECECOLORDARK = mycolors.DARKGREEN
PIECEGHOSTCOLOR = mycolors.LIGHTGRAY
# COLORSCHEMES
purpleScheme = {'color' : (102, 0, 204), 'light' : (178, 102, 255), 'dark' : (51, 0, 102)}
greenScheme = {'color' : (0, 255, 0), 'light' : (102, 255, 102), 'dark' : (0, 102, 0)}
redScheme = {'color' : (255, 0, 0), 'light' : (255, 102, 102), 'dark' : (102, 0, 0)}
blueScheme = {'color' : (0, 0, 255), 'light' : (102, 102, 255), 'dark' : (0, 0, 102)}
orangeScheme = {'color' : (255, 178, 102), 'light' : (255, 128, 0), 'dark' : (102, 51, 0)}
cyanScheme = {'color' : (0, 255, 255), 'light' : (102, 255, 255), 'dark' : (0, 102, 102)}
yellowScheme = {'color' : (255, 255, 0), 'light' : (255, 255, 102), 'dark' : (102, 102, 0)}
# fonts
FONT = 'freesansbold.ttf'
FONTCOLOR = mycolors.WHITE
FONTSIZE = CELLSIZE
# data representations
BLANK = 0
FILLED = 1
UP = 10
DOWN = 11
RIGHT = 12
LEFT = 13
UPLEFT = 14
UPRIGHT = 15
DOWNLEFT = 16
DOWNRIGHT = 17
JIGGLEDIRECTIONS = [UP, LEFT, RIGHT, DOWN]
CW = 18
ACW = 19
ONE80 = 20
ROTINVERSE = {CW : ACW, ACW : CW, ONE80 : ONE80}
purpleKey = 21
greenKey = 22
redKey = 23
blueKey = 24
orangeKey = 25
cyanKey = 26
yellowKey = 27
COLORSCHEMEMAP = {purpleKey : purpleScheme, greenKey : greenScheme, redKey : redScheme, blueKey : blueScheme, orangeKey : orangeScheme, cyanKey : cyanScheme, yellowKey : yellowScheme}

def main():
    pygame.init()
    tetris = Tetris()
    tetris.runTextScreen('press any key to start')
    while True:
        time = None
        time = tetris.run() # run is a single round of tetris
        if time == None:
            tetris.runTextScreen('Game over! Press any key to try again')
        else:
            tetris.runTextScreen('Well played! Time Taken: {:.3f}'.format(time))
        

class Tetris:

    def __init__(self):
        self.display = pygame.display.set_mode((WINDW, WINDH))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()

    def runTextScreen(self, msg):
        text = getText(msg)
        center = (WINDW // 2, WINDH // 2)
        rect = text.get_rect()
        rect.center = center

        self.display.fill(TEXTSCREENCOLOR)
        self.display.blit(text, rect)
        pygame.display.update()
        # short wait, so that player does not unintentionally press key
        pygame.time.wait(1000)
        pygame.event.get()
        while True:
            for event in pygame.event.get():
                if event.type == KEYUP:
                    return
            self.clock.tick(FPS)
        
        
    def run(self):
        # grid related attr
        self.grid = [[BLANK for col in range(NUMCOLS)] for row in range(NUMROWS)] # array of rows
        self.gridRect = pygame.Rect(XMARGIN, YMARGIN, NUMCOLS*CELLSIZE, NUMROWS*CELLSIZE)
        self.gridSurf = pygame.Surface((NUMCOLS * CELLSIZE, NUMROWS * CELLSIZE))
        # KeyTimer Objects
        self.leftKey = KeyTimer()
        self.rightKey = KeyTimer()
        self.downKey = KeyTimer()
        self.gravityKey = KeyTimer()
        self.gravityKey.pressDown() # turn on gravity
        # piece generator
        self.pieceGenerator = pieceGenerator()
        # piece attr
        self.curPiece = self.getNewPiece()
        self.curPiece.moveTo(NUMCOLS//2, 0)
        self.pieceQueue = [self.getNewPiece() for i in range(NUMPREVIEWS)]
        self.swapPiece = None
        # time and lines
        self.startTime = time.time()
        self.linesLeft = NUMLINES

        # draw initial screen
        self.display.fill(BGCOLOR)
        self.drawGridSurf()
        self.drawGrid()
        self.drawCurPiece()
        self.drawPreviews()
        self.drawSwap()
        
        while True:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == SHIFTLEFT: # shift left
                        self.tryShift(LEFT, 1)
                        self.leftKey.pressDown()
                    elif event.key == SHIFTRIGHT: # shift right
                        self.tryShift(RIGHT, 1)
                        self.rightKey.pressDown()
                    elif event.key in [ROTCW, ROTACW, ROTONE80]: # rotations
                        if event.key == ROTCW:
                            self.tryRotate(CW)
                        elif event.key == ROTACW:
                            self.tryRotate(ACW)
                        elif event.key == ROTONE80:
                            self.tryRotate(ONE80)
                    elif event.key == SOFTDROP: # soft drop
                        self.tryShift(DOWN, 1)
                        self.downKey.pressDown()
                    elif event.key == HARDDROP: # hard drop
                        self.tryShift(DOWN, MAXSHIFTDOWNWARDS)
                        placed = self.placePiece() # exit point
                        if not placed:
                            return
                        self.gravityKey.resetTimer()
                    elif event.key == SWAP: # swap
                        self.swap()
                elif event.type == KEYUP:
                    if event.key == SHIFTLEFT:
                        self.leftKey.release()
                    elif event.key == SHIFTRIGHT:
                        self.rightKey.release()
                    elif event.key == SOFTDROP:
                        self.downKey.release()

            # compulsory checks (opted to allow holding to flush multiple times (*))
            if self.gravityKey.getTimeHeld() > GRAVITYDELAY:
                moved = self.tryShift(DOWN, 1)
                self.gravityKey.resetTimer()
                if not moved:
                    placed = self.placePiece()
                    if not placed:
                        return
            if self.leftKey.isDown and self.leftKey.getTimeHeld() > FLUSHDELAY:
                self.tryShift(LEFT, MAXSHIFTSIDEWAYS)
                #(*) self.leftKey.release() # after a flush, further holding is ignored
            if self.rightKey.isDown and self.rightKey.getTimeHeld() > FLUSHDELAY:
                self.tryShift(RIGHT, MAXSHIFTSIDEWAYS)
                #(*) self.rightKey.release() # after a flush, further holding is ignored
            if self.downKey.isDown and self.downKey.getTimeHeld() > SOFTDROPDELAY:
                self.tryShift(DOWN, 1)
                self.downKey.resetTimer()
            if self.linesLeft <= 0:
                return time.time() - self.startTime

            # draw to Screen
            self.drawGrid()
            self.drawGhostPiece()
            self.drawCurPiece()
            self.drawTimeAndLines()
            pygame.display.update()
            self.clock.tick(FPS)


    ##### DRAWING #####
    def drawBlank(self, x, y):
        # draw empty space at box coords (x, y) (dont need to be on grid)
        pX, pY = gridToPixel(x, y)
        pygame.draw.rect(self.display, GRIDCOLOR, (pX, pY, CELLSIZE, CELLSIZE))
    def _drawFilled(self, pX, pY, colorScheme):
        pygame.draw.rect(self.display, colorScheme['dark'], (pX, pY, CELLSIZE, CELLSIZE))
        pygame.draw.rect(self.display, colorScheme['light'], (pX, pY, CELLSIZE - CELLBORDER, CELLSIZE - CELLBORDER))
        pygame.draw.rect(self.display, colorScheme['color'], (pX + CELLBORDER, pY + CELLBORDER, CELLSIZE - 2 * CELLBORDER, CELLSIZE - 2 * CELLBORDER))
    def drawFilled(self, x, y, colorScheme):
        # draw a filled cell at box coords (x, y)
        pX, pY = gridToPixel(x, y)
        self._drawFilled(pX, pY, colorScheme)
    def drawGhost(self, x, y):
        pX, pY = gridToPixel(x, y)
        pygame.draw.rect(self.display, PIECEGHOSTCOLOR, (pX, pY, CELLSIZE, CELLSIZE))
        pygame.draw.rect(self.display, GRIDCOLOR, (pX + GHOSTBORDER, pY + GHOSTBORDER, CELLSIZE - 2 * GHOSTBORDER, CELLSIZE - 2 * GHOSTBORDER))
    def drawGridSurf(self):
        # draw gridSurf
        self.gridSurf.fill(GRIDCOLOR)
        for c in range(NUMCOLS):
            for r in range(NUMROWS):
                if self.grid[r][c] != BLANK:
                    pX = c * CELLSIZE
                    pY = r * CELLSIZE
                    colorKey = self.grid[r][c]
                    colorScheme = COLORSCHEMEMAP[colorKey]
                    pygame.draw.rect(self.gridSurf, colorScheme['dark'], (pX, pY, CELLSIZE, CELLSIZE)) # not repeated code bc _drawFilled draws to main surface
                    pygame.draw.rect(self.gridSurf, colorScheme['light'], (pX, pY, CELLSIZE - CELLBORDER, CELLSIZE - CELLBORDER))
                    pygame.draw.rect(self.gridSurf, colorScheme['color'], (pX + CELLBORDER, pY + CELLBORDER, CELLSIZE - 2 * CELLBORDER, CELLSIZE - 2 * CELLBORDER))
    def drawGrid(self):
        # blit gridSurf to display
        self.display.blit(self.gridSurf, (self.gridRect.topleft))
    def drawPiece(self, piece, ignore=False):
        if ignore: # include check for on grid
            for cell in piece.occupiedCells:
                if isOnGrid(cell[0], cell[1]):
                    self.drawFilled(cell[0], cell[1], piece.colorScheme)
        else:
            for cell in piece.occupiedCells:
                self.drawFilled(cell[0], cell[1], piece.colorScheme)
    def drawCurPiece(self):
        self.drawPiece(self.curPiece, True)
    def drawGhostPiece(self):
        dist = 0
        while self.tryShift(DOWN, 1):
            dist += 1
        # draw the piece
        for cell in self.curPiece.occupiedCells:
            if isOnGrid(cell[0], cell[1]): # only draw whats on the grid
                self.drawGhost(cell[0], cell[1])
        # shift piece back up
        self.tryShift(UP, dist)
    def drawPreviews(self):
        #draw preview rects
        for x, y in PREVIEWRECTPIXELCOORDS:
            pygame.draw.rect(self.display, GRIDCOLOR, (x, y, PREVIEWBOXSIZE, PREVIEWBOXSIZE))
        # draw pieces
        for piece, coord, in zip(self.pieceQueue, PREVIEWGRIDCOORDS):
            piece.moveTo(coord[0], coord[1]) # position piece correctly
            self.drawPiece(piece)
    def drawSwap(self):
        pygame.draw.rect(self.display, GRIDCOLOR, (SWAPRECTXMARGIN, SWAPRECTYMARGIN, SWAPBOXSIZE, SWAPBOXSIZE))
        if self.swapPiece != None:
            self.drawPiece(self.swapPiece)
    def drawTimeAndLines(self):
        elapsedTime = time.time() - self.startTime
        timeText = getTimeText(elapsedTime)
        rect1 = timeText.get_rect()
        rect1.midbottom = TEXTBOXRECT.center

        linesLeftText = getText('Lines Left: {0: >2}'.format(self.linesLeft))
        rect2 = linesLeftText.get_rect()
        rect2.midtop = TEXTBOXRECT.center

        pygame.draw.rect(self.display, GRIDCOLOR, TEXTBOXRECT)
        self.display.blit(timeText, rect1)
        self.display.blit(linesLeftText, rect2)
                    

    ##### HELPER #####
    def copyToGrid(self, piece):
        # returns whether piece was fully copied to grid
        if not all(isOnGrid(cell[0], cell[1]) for cell in piece.occupiedCells):
            return False
        for cell in piece.occupiedCells: # fill up grid with the piece
            self.grid[cell[1]][cell[0]] = piece.key
        self.drawGridSurf() # update copies of gridSurf
        return True
    def isCurPieceWithinGrid(self, tight=True):
        return all(isOnGrid(cell[0], cell[1], tight) for cell in self.curPiece.occupiedCells)
    def isCurPieceFree(self): # free of collision; all the cells of piece are either 1. off the grid or 2. on a BLANK
        return all(  (not isOnGrid(cell[0], cell[1])) or self.grid[cell[1]][cell[0]] == BLANK for cell in self.curPiece.occupiedCells  )
    def isCurPieceValid(self, tight=True):
        return self.isCurPieceWithinGrid(tight) and self.isCurPieceFree()
    def tryShift(self, direction, dist=1):
        # returns whether shift was successful
        for i in range(dist):
            self.curPiece.shift(direction, 1)
            if not self.isCurPieceValid(False): # tight=False because piece is free to move even above grid
                self.curPiece.shift(direction, -1)
                return False
        return True
    def tryRotate(self, amount):
        self.curPiece.rotate(amount)
        if not self.isCurPieceValid(False): # note tight=False
            # try jiggling the piece
            for direction in JIGGLEDIRECTIONS:
                for dist in [1, 2]: # can shift up to 2 cells away
                    self.curPiece.shift(direction, dist)
                    if self.isCurPieceValid():
                        return # accept first available, stop execution
                    else:
                        self.curPiece.shift(direction, -1)
            # undo initial rotation
            self.curPiece.rotate(ROTINVERSE[amount])
    def placePiece(self): # opted to allow key presses to affect next piece by NOT calling release of KeyTimers
        # returns whether piece was successfully placed
        copied = self.copyToGrid(self.curPiece)
        self.deleteFilledRows()
        self.getNextPiece()
        return copied
    def getNewPiece(self):
        # returns a 'random' Piece positioned at [0, 0]
        '''
        x = random.randint(0, 6)
        if x == 0:
            p = TPiece()
        elif x == 1:
            p = SPiece()
        elif x == 2:
            p = ZPiece()
        elif x == 3:
            p = JPiece()
        elif x == 4:
            p = LPiece()
        elif x == 5:
            p = IPiece()
        elif x == 6:
            p = OPiece()
        '''
        piece = next(self.pieceGenerator)
        # rotate piece by a random amount
        amount = random.choice([CW, ACW, ONE80])
        piece.rotate(amount)
        return piece
    def getNextPiece(self):
        # get next Piece of pieceQueue and position it
        self.curPiece = self.pieceQueue.pop(0)
        self.curPiece.moveTo(STARTCOORDS[0], STARTCOORDS[1])
        # refill pieceQueue
        self.pieceQueue.append(self.getNewPiece())
        # re draw the previews
        self.drawPreviews()
    def deleteFilledRows(self):
        self.grid = [row for row in self.grid if not (BLANK not in row)]
        self.linesLeft -= NUMROWS - len(self.grid)
        while len(self.grid) < NUMROWS:
            self.grid.insert(0, [BLANK] * NUMCOLS)
        self.drawGridSurf()
    def swap(self):
        if self.swapPiece == None:
            self.swapPiece = self.curPiece
            self.swapPiece.moveTo(SWAPGRIDCOORDS[0], SWAPGRIDCOORDS[1])
            self.getNextPiece()
        else:
            self.swapPiece, self.curPiece = self.curPiece, self.swapPiece
            self.swapPiece.moveTo(SWAPGRIDCOORDS[0], SWAPGRIDCOORDS[1])
            self.curPiece.moveTo(STARTCOORDS[0], STARTCOORDS[1])
        self.drawSwap()
    
        

##### HELPER #####
def pieceGenerator():
    while True:
        bag = [TPiece(), SPiece(), ZPiece(), JPiece(), LPiece(), IPiece(), OPiece()]
        random.shuffle(bag)
        for piece in bag:
            yield piece

def getText(msg):
    font = pygame.font.Font(FONT, FONTSIZE)
    text = font.render(msg, True, FONTCOLOR, GRIDCOLOR)
    return text
def getTimeText(n):
    msg = '{:.3f}'.format(n)
    return getText(msg)
def gridToPixel(x, y):
    return x * CELLSIZE + XMARGIN, y * CELLSIZE + YMARGIN
def isOnGrid(x, y, tight=True):
    if tight:
        yBound = 0
    else:
        yBound = -3
    return (0 <= x and x < NUMCOLS) and (yBound <= y and y < NUMROWS)



##### OBJECTS #####
class Piece:
    orientationMap = {UP : RIGHT, RIGHT : DOWN, DOWN : LEFT, LEFT : UP, UPRIGHT : DOWNRIGHT, DOWNRIGHT : DOWNLEFT, DOWNLEFT : UPLEFT, UPLEFT : UPRIGHT}

    def __init__(self):
        self.center = [0, 0]
        self.orientation = UP
        self.relativeCells = None
        self.occupiedCells = None
        self.colorScheme = None

    @staticmethod
    def _getAdj(loc, direction, d=1):
        x, y = loc
        if direction == UP:
            return [x, y - d]
        elif direction == DOWN:
            return [x, y + d]
        elif direction == LEFT:
            return [x - d, y]
        elif direction == RIGHT:
            return [x + d, y]
        elif direction == UPRIGHT:
            return [x + d, y - d]
        elif direction == DOWNRIGHT:
            return [x + d, y + d]
        elif direction == DOWNLEFT:
            return [x - d, y + d]
        elif direction == UPLEFT:
            return [x - d, y - d]

    def _rotateOrientation(self):
        self.orientation = Piece.orientationMap[self.orientation]

    def _rotateRelativeCells(self):
        for relativeCell in self.relativeCells:
            relativeCell[0] = Piece.orientationMap[relativeCell[0]]

    def _rotateClockwise(self):
        self._rotateOrientation()
        self._rotateRelativeCells()

    def _genOccupiedCells(self):
        self.occupiedCells = [Piece._getAdj(self.center, rCell[0], rCell[1]) for rCell in self.relativeCells]

    def rotate(self, amount):
        if amount == CW:
            self._rotateClockwise()
        elif amount == ONE80:
            self._rotateClockwise()
            self._rotateClockwise()
        elif amount == ACW:
            self._rotateClockwise()
            self._rotateClockwise()
            self._rotateClockwise()
        self._genOccupiedCells()

    def shift(self, direction, d=1):
        self.center = Piece._getAdj(self.center, direction, d)
        self._genOccupiedCells()

    def moveTo(self, x, y):
        self.center = [x, y]
        self._genOccupiedCells()



class TPiece(Piece):
    def __init__(self):
        super().__init__()
        self.relativeCells = [[UP, 0],[LEFT, 1], [UP, 1], [RIGHT, 1]]
        self._genOccupiedCells()
        self.colorScheme = purpleScheme
        self.key = purpleKey

class SPiece(Piece):
    def __init__(self):
        super().__init__()
        self.relativeCells = [[UP, 0],[LEFT, 1], [UP, 1], [UPRIGHT, 1]]
        self._genOccupiedCells()
        self.colorScheme = greenScheme
        self.key = greenKey

class ZPiece(Piece):
    def __init__(self):
        super().__init__()
        self.relativeCells = [[UP, 0],[UPLEFT, 1], [UP, 1], [RIGHT, 1]]
        self._genOccupiedCells()
        self.colorScheme = redScheme
        self.key = redKey
        
class JPiece(Piece):
    def __init__(self):
        super().__init__()
        self.relativeCells = [[UP, 0],[UP, 1], [DOWN, 1], [DOWNLEFT, 1]]
        self._genOccupiedCells()
        self.colorScheme = blueScheme
        self.key = blueKey
        
class LPiece(Piece):
    def __init__(self):
        super().__init__()
        self.relativeCells = [[UP, 0],[UP, 1], [DOWN, 1], [DOWNRIGHT, 1]]
        self._genOccupiedCells()
        self.colorScheme = orangeScheme
        self.key = orangeKey
        
class IPiece(Piece):
    def __init__(self):
        super().__init__()
        self.relativeCells = [[UP, 0],[LEFT, 2], [LEFT, 1], [RIGHT, 1]]
        self._genOccupiedCells()
        self.colorScheme = cyanScheme
        self.key = cyanKey
        
class OPiece(Piece):
    def __init__(self):
        super().__init__()
        self.relativeCells = [[UP, 0],[LEFT, 1], [UP, 1], [UPLEFT, 1]]
        self._genOccupiedCells()
        self.colorScheme = yellowScheme
        self.key = yellowKey

    def rotate(self, amount):
        pass
        
class KeyTimer:

    def __init__(self):
        self.isDown = False
        self.pressedDownAt = None

    def pressDown(self):
        self.isDown = True
        self.pressedDownAt = time.time()

    def release(self):
        self.isDown = False
        self.pressedDownAt = None

    def resetTimer(self):
        self.pressedDownAt = time.time()

    def getTimeHeld(self):
        return time.time() - self.pressedDownAt
   


if __name__ == '__main__':
    main()



