"""
Tetris made with pygame 2.0.0, earlier versions don't run on the latest version of OSX,
as such cannot guarantee that it works on earlier versions of pygame
code by Dylan Moody, you can find my Github at https://github.com/dylanmoody
I will attempt to be as thorough as possible in my commenting, but if you have any questions or suggestions
feel free to email me at dmoody@idtech.com

CONTROLS:
x: flip clockwise
z: flip counterclockwise
space: store current block
right arrow: move right
left arrow: move left
down arrow: fall faster

Enjoy!

"""

# import libraries, pygame should be 2.0.0
import pygame
import random
import sys
from block import *


# This function will return a random subclass of block as defined in the block.py file
def create_rand_block():
    randNum = random.randint(1, 7)

    if randNum == 1:
        return I((10, 100, 100), 3, blockSize)
    if randNum == 2:
        return J((10, 10, 220), 3, blockSize)
    if randNum == 3:
        return L((150, 100, 10), 3, blockSize)
    if randNum == 4:
        return O((150, 150, 10), 0, blockSize)
    if randNum == 5:
        return S((10, 150, 10), 3, blockSize)
    if randNum == 6:
        return T((100, 10, 150), 3, blockSize)
    if randNum == 7:
        return Z((150, 10, 10), 3, blockSize)


# this function cycles to the next of the blocks in waiting
# the next block list, and the surface the next block list gets drawn on
# it swaps the first element of the list to the current block then removes it, adds a new block and shifts all the
# blocks up
def take_next(nextB, nextSurf):
    currentB = nextB[0]
    currentB.set_pos(leftSide + blockSize * 3, topSide)
    currentB.set_size(blockSize)
    nextB.pop(0)
    nextB.append(create_rand_block())
    nextB[2].set_size(blockSize // 2)
    nextSurf.fill((0, 0, 0))
    for i in range(3):
        nextB[i].set_pos(0, blockSize * i * 2)
        nextB[i].draw_block(nextSurf)
    return currentB, nextB


# this function is for the stored block it needs the currentBlock, the storedBlock and the list of next blocks
# it needs the list of nextBlocks for when nothing is currently stored, the behavior in this scenario is storing a
# mini version of the currentBlock then cycling the next block list using take_next()
# if there is already a stored block, the stored block gets set to the normal size and placed at the middle top
# and the current block gets downsized and placed at (0,0) for display on the stored block surface
def store_block(current, stored, nextB):
    current.set_state(0)
    if stored is None:
        current.set_size(blockSize // 2)
        current.set_pos(0, 0)
        stored = current
        current, nextB = take_next(nextB, nextSurface)
    else:
        stored.set_size(blockSize)
        stored.set_pos(leftSide + blockSize * 3, topSide)
        temp = stored
        current.set_size(blockSize // 2)
        current.set_pos(0, 0)
        stored = current
        current = temp
    return current, stored, nextB


pygame.init()

# this variable will determine the size of everything else on the screen, and even the screen size itself
# it will be used everywhere
# game works best with sizes: 20, 30, 40
blockSize = 30

# create the screensize, board size, and board edge locations
screen_size = width, height = (blockSize * 16, blockSize * 24)
leftSide = blockSize * 2
boardWidth = blockSize * 10
rightSide = leftSide + boardWidth
topSide = blockSize * 2
boardHeight = blockSize * 20
bottomSide = topSide + boardHeight

# PyGame works using Surfaces. Every shape that gets drawn goes on a Surface.
display_surface = pygame.display.set_mode(screen_size)

# create a ticker that can be used to set a frame rate
clock = pygame.time.Clock()

# this is the surface that the currently falling block gets drawn on
# it needs to be filled with the color key color and have the block drawn on at every iteration
# the mask is for collision detection
currentSurface = pygame.Surface((width, height))
currentSurface.fill((0, 0, 0))
currentSurface.set_colorkey((0, 0, 0))
currentMask = pygame.mask.from_surface(currentSurface)

# this is the surface that blocks get added to after they stop falling
# the mask needs to be updated every time a new block is added
savedBlocks = pygame.Surface((width, height))
savedBlocks.fill((0, 0, 0))
savedBlocks.set_colorkey((0, 0, 0))
savedBlocksMask = pygame.mask.from_surface(savedBlocks)

# this surface is for when a row needs to be cleared
# it saves a record of the savedBlock surface so it can be redrawn after the savedBlocks surface is cleared
savedBlocksTemp = pygame.Surface((width, height))
savedBlocksTemp.fill((0, 0, 0))
savedBlocksTemp.set_colorkey((0, 0, 0))

# this is a gray line that will be drawn on the bottom of the screen so blocks can land on it
# it never changes and the mask never needs updating
screenBottom = pygame.Surface((boardWidth, 5))
screenBottom.fill((85, 85, 85))
bottomMask = pygame.mask.from_surface(screenBottom)

# this is a red line that never gets drawn on the screen, it is used alongside the savedBlocks layer to check if
# any rows are full
rowCheck = pygame.Surface((boardWidth, 1))
rowCheck.fill((250, 0, 0))
checkMask = pygame.mask.from_surface(rowCheck)

# similar to the screen bottom layer, except the sides of the screen this time
# both the surface and the mask are never updated again
screenSides = pygame.Surface((width, height))
screenSides.fill((0, 0, 0))
screenSides.set_colorkey((0, 0, 0))
screenSides.fill((85, 85, 85), rect=[leftSide-5, topSide, 5, boardHeight])
screenSides.fill((85, 85, 85), rect=[rightSide, topSide, 5, boardHeight])
sidesMask = pygame.mask.from_surface(screenSides)

# this is a small surface that fits exactly three shrunk blocks, it will display to the top right of the screen
# it shows the player which blocks will fall next
nextSurface = pygame.Surface((blockSize * 2, blockSize * 6))
nextSurface.fill((0, 0, 0))
nextSurface.set_colorkey((0, 0, 0))

# this is a small surface that stores exactly one shrunk block, it will display on the bottom right of the screen
# it shows the player which block they are currently storing
storedSurface = pygame.Surface((blockSize * 2, blockSize * 2))
storedSurface.fill((0, 0, 0))
storedSurface.set_colorkey((0, 0, 0))

# currentBlock stores the currently falling block, next block is a list of the next three blocks to fall
currentBlock = create_rand_block()
nextBlock = list()
nextBlock.append(create_rand_block())
nextBlock.append(create_rand_block())
nextBlock.append(create_rand_block())
for i in range(3):
    nextBlock[i].set_pos(0, blockSize * i * 2)
    nextBlock[i].set_size(blockSize // 2)
    nextBlock[i].draw_block(nextSurface)

# stored block stores the currently held block
# holdTime is the timer that lets the blocks be moved for 60 frames after landing
# stateChange keeps track of how the state of the current block changed during the current frame
# playing will be True until the blocks are stacked too high
# check row is the row number that will be checked each turn, it goes up to 20
storedBlock = None
holdTime = 0
stateChange = 0
playing = True
checkRow = 2
speed = blockSize // 10

while playing:
    # force a frame rate of 60
    clock.tick(60)

    # zoom makes the block fall faster, get pressed is used so the down arrow can be held down
    zoom = 1
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        zoom = 2

    # check for certain events every frame
    for event in pygame.event.get():
        # close the window if the player tries to close the window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # close the window with escape key
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # flip block clockwise with x
            elif event.key == pygame.K_x:
                stateChange = 1
            # flip block counterclockwise with z
            elif event.key == pygame.K_z:
                stateChange = -1
            # if the block wouldn't be inside something else move right one block with right arrow
            elif event.key == pygame.K_RIGHT:
                if not savedBlocksMask.overlap(currentMask, (blockSize, 0)) \
                        and not sidesMask.overlap(currentMask, (blockSize, 0)):
                    currentBlock.block_move(blockSize)
            # and left one block with left arrow
            elif event.key == pygame.K_LEFT:
                if not savedBlocksMask.overlap(currentMask, (-blockSize, 0)) \
                        and not sidesMask.overlap(currentMask, (-blockSize, 0)):
                    currentBlock.block_move(-blockSize)
            # store current block with space
            elif event.key == pygame.K_SPACE:
                currentBlock, storedBlock, nextBlock = store_block(currentBlock, storedBlock, nextBlock)
                storedSurface.fill((0, 0, 0))
                storedBlock.draw_block(storedSurface)

    # background color
    display_surface.fill((0, 0, 0))

    # if state changed, flip block in that direction, then check if that flip caused the current block to overlap
    # if it did, flip it back
    if stateChange == 1 or stateChange == -1:
        currentBlock.swap_state( stateChange )
        currentSurface.fill((0, 0, 0))
        currentBlock.draw_block( currentSurface )
        currentMask = pygame.mask.from_surface( currentSurface )
        if currentMask.overlap(bottomMask, (leftSide, bottomSide)) or currentMask.overlap(savedBlocksMask, (0, 0)) \
                or currentMask.overlap(sidesMask, (0, 0)):
            currentBlock.swap_state( stateChange * -1 )
            stateChange = 0

    # draw current block and update collision mask
    if stateChange == 0:
        currentSurface.fill((0, 0, 0))
        currentBlock.draw_block(currentSurface)
        currentMask = pygame.mask.from_surface(currentSurface)

    stateChange = 0

    # if moving the block would result in the block being inside something:
    # move the block down one pixel at a time until it is resting on top of the something, then start holding
    if currentMask.overlap(bottomMask, (leftSide, bottomSide-speed * zoom)) or currentMask.overlap(savedBlocksMask, (0, -speed * zoom-1)):
        while not currentMask.overlap(bottomMask, (leftSide, bottomSide-1)) and not currentMask.overlap(savedBlocksMask, (0, -1)):
            currentBlock.move(1)
            currentSurface.fill((0, 0, 0))
            currentBlock.draw_block(currentSurface)
            currentMask = pygame.mask.from_surface(currentSurface)
        holdTime += 1
    else:
        holdTime = 0
        currentBlock.move(zoom*speed)

    # have held for 60 frames, draw the current block on the savedBlocks surface and get a new currentBlock
    if holdTime == 60:
        currentBlock.draw_block(savedBlocks)
        savedBlocksMask = pygame.mask.from_surface(savedBlocks)
        currentBlock, nextBlock = take_next(nextBlock, nextSurface)
        holdTime = 0

    # check one row each frame, if a row is full store the blocks above the row on a temporary surface
    # then store the block below it on a temporary surface and wipe the saved blocks surface clean
    # redraw the temporary surface onto the savedBlocks surface and wipe the temporary surface clean
    # lastly update the mask
    # note that we don't need to check the full 20 rows because the top two result in a game over
    if savedBlocksMask.overlap_area(checkMask, (leftSide, checkRow * blockSize + topSide + 1)) == blockSize*10:
        savedBlocksTemp.blit(savedBlocks, (0, 0), area=pygame.Rect(leftSide, topSide, boardWidth, checkRow * blockSize))
        savedBlocksTemp.blit(savedBlocks, (0, checkRow * blockSize), area=pygame.Rect(leftSide, topSide + (checkRow + 1) * blockSize, boardWidth, (20 - checkRow) * blockSize))
        savedBlocks.fill((0, 0, 0))
        savedBlocks.blit(savedBlocksTemp, (leftSide, topSide + blockSize))
        savedBlocksTemp.fill((0, 0, 0))
        savedBlocksMask = pygame.mask.from_surface(savedBlocks)
    checkRow += 1
    if checkRow > 20:
        checkRow = 2

    # check if the player has built their tetris tower too high, and end the game if they have
    if savedBlocksMask.overlap_area(checkMask, (leftSide, topSide + blockSize)) > 0:
        playing = False

    # draw all of the surfaces onto the screen
    display_surface.blit(screenSides, (0, 0))
    display_surface.blit(screenBottom, (leftSide, bottomSide))
    display_surface.blit(currentSurface, (0, 0))
    display_surface.blit(savedBlocks, (0, 0))
    display_surface.blit(nextSurface, (rightSide + blockSize, topSide))
    display_surface.blit(storedSurface, (rightSide + blockSize, bottomSide - blockSize * 2))
    # display_surface.blit(rowCheck, (leftSide, bottomSide-10))

    # update the screen every frame
    pygame.display.flip()


# this is only for displaying a game over message after the game is over
while not playing:
    # force a frame rate of 60
    clock.tick(60)

    # check the events every frame.
    for event in pygame.event.get():
        # close the window if the player tries to close the window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # close the window with escape key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # only need to draw the game over and the background
    display_surface.fill((0, 0, 0))
    display_surface.blit(pygame.font.Font(None, blockSize * 3).render("GAME OVER", True, (255, 255, 255), (0, 0, 0)), (blockSize + blockSize // 2, boardHeight // 2))

    # update the screen every frame
    pygame.display.flip()