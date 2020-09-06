# coded by Dylan Moody
# the main block class for the tetris game mainly for use as a parent class
class Block:
    def __init__(self, newColor, newMaxState, blockSize):
        self.pos = [blockSize * 5, blockSize * 2]
        self.color = newColor
        self.size = blockSize
        self.state = 0
        self.maxState = newMaxState
        return

    # increment state by num, wrap it back around if it becomes too high or too low
    def swap_state(self, num):
        self.state += num
        if self.state < 0:
            self.state = self.maxState
        elif self.state > self.maxState:
            self.state = 0
        return

    # cause block to fall
    def move(self, speed):
        self.pos[1] += speed
        return

    # this move is for moving side to side
    def block_move(self, num):
        self.pos[0] += num
        return

    # mainly used for storing blocks in the original state
    def set_state(self, num):
        self.state = num
        return

    # resize the block, mainly used for stored block and next blocks which are half size
    def set_size(self, blockSize):
        self.size = blockSize
        return

    def get_pos(self):
        return self.pos

    def set_pos(self, x, y):
        self.pos = [x, y]
        return


"""
the rest of this file will be the various letter block which all use the main block class as a parent
each one has a draw_block function which defines how the block should look in each state 
the draw will happen onto the surface passed as a parameter, sometimes two draws are needed for the full block
"""


class I(Block):
    def draw_block(self, surf):
        if self.state == 0:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1]+self.size, self.size*4, self.size])
        if self.state == 1:
            surf.fill(self.color, rect=[self.pos[0]+self.size*3, self.pos[1], self.size, self.size*4])
        if self.state == 2:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1]+self.size*2, self.size*4, self.size])
        if self.state == 3:
            surf.fill(self.color, rect=[self.pos[0]+self.size*2, self.pos[1], self.size, self.size*4])
        return


class J(Block):
    def draw_block(self, surf):
        if self.state == 0:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1], self.size, self.size*2])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1]+self.size, self.size*2, self.size])
        elif self.state == 1:
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1], self.size*2, self.size])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1]+self.size, self.size, self.size*2])
        elif self.state == 2:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1]+self.size, self.size*2, self.size])
            surf.fill(self.color, rect=[self.pos[0]+self.size*2, self.pos[1]+self.size, self.size, self.size*2])
        elif self.state == 3:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1]+self.size*2, self.size*2, self.size])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1], self.size, self.size*2])
        return


class L(Block):
    def draw_block(self, surf):
        if self.state == 0:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1]+self.size, self.size*2, self.size])
            surf.fill(self.color, rect=[self.pos[0]+self.size*2, self.pos[1], self.size, self.size*2])
        elif self.state == 1:
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1], self.size, self.size*2])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1]+self.size*2, self.size*2, self.size])
        elif self.state == 2:
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1]+self.size, self.size*2, self.size])
            surf.fill(self.color, rect=[self.pos[0], self.pos[1]+self.size, self.size, self.size*2])
        elif self.state == 3:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1], self.size*2, self.size])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1]+self.size, self.size, self.size*2])
        return


class O(Block):
    def draw_block(self, surf):
        surf.fill(self.color, rect=[self.pos[0], self.pos[1], self.size*2, self.size*2])
        return


class S(Block):
    def draw_block(self, surf):
        if self.state == 0:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1]+self.size, self.size*2, self.size])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1], self.size*2, self.size])
        if self.state == 1:
            surf.fill(self.color, rect=[self.pos[0]+self.size*2, self.pos[1]+self.size, self.size, self.size*2])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1], self.size, self.size*2])
        if self.state == 2:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1]+self.size*2, self.size*2, self.size])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1]+self.size, self.size*2, self.size])
        if self.state == 3:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1], self.size, self.size*2])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1]+self.size, self.size, self.size*2])
        return


class T(Block):
    def draw_block(self, surf):
        if self.state == 0:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1]+self.size, self.size*3, self.size])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1], self.size, self.size])
        if self.state == 1:
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1], self.size, self.size*3])
            surf.fill(self.color, rect=[self.pos[0]+self.size*2, self.pos[1] + self.size, self.size, self.size])
        if self.state == 2:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1]+self.size, self.size*3, self.size])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1]+self.size*2, self.size, self.size])
        if self.state == 3:
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1], self.size, self.size*3])
            surf.fill(self.color, rect=[self.pos[0], self.pos[1] + self.size, self.size, self.size])
        return


class Z(Block):
    def draw_block(self, surf):
        if self.state == 0:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1], self.size*2, self.size])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1]+self.size, self.size*2, self.size])
        if self.state == 1:
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1]+self.size, self.size, self.size*2])
            surf.fill(self.color, rect=[self.pos[0]+self.size*2, self.pos[1], self.size, self.size*2])
        if self.state == 2:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1]+self.size, self.size*2, self.size])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1]+self.size*2, self.size*2, self.size])
        if self.state == 3:
            surf.fill(self.color, rect=[self.pos[0], self.pos[1]+self.size, self.size, self.size*2])
            surf.fill(self.color, rect=[self.pos[0]+self.size, self.pos[1], self.size, self.size*2])
        return
