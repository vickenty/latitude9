import random

import items

class Cell (object):
    HIDDEN = 0
    MEMORY = 1
    LIT = 2

    def __init__(self, x=0, y=0, visible=HIDDEN):
        self.x = x
        self.y = y
        self.visible = visible
        self.item = None
        self.trap = None

class Wall(Cell):
    name = 'wall'
    walkable = False

class Floor(Cell):
    name = 'floor'
    walkable = True

def clamped_range(center, delta, minv, maxv):
    delta = int(delta + 0.5)
    return xrange(max(minv, center - delta), min(maxv, center + delta + 1))

class Level (object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.data = [None] * self.w * self.h

        self.dirty_list = []

    def __getitem__(self, key):
        return self.data[self.offset(*key)]

    def __setitem__(self, key, cell):
        cell.x, cell.y = key
        self.data[self.offset(*key)] = cell
        self.dirty_list.append(cell)

    def offset(self, x, y):
        return y * self.w + x

    def wipe(self):
        self.dirty_list = []

    def update_visibility(self, cx, cy, radius=6.5):
        r2 = radius**2
        for x in clamped_range(cx, radius, 0, self.w):
            for y in clamped_range(cy, radius, 0, self.h):
                cell = self[x, y]
                d2 = (x - cx)**2 + (y - cy)**2
                if cell:
                    if d2 <= r2:
                        cell.visible = cell.LIT
                    else:
                        cell.visible = cell.visible and cell.MEMORY

                    self.dirty_list.append(cell)

class Dummy (Level):
    def __init__(self, w, h):
        super(Dummy, self).__init__(w, h)

    def generate(self):
        for y in [0, self.h - 1]:
            for x in range(0, self.w):
                self[x, y] = Wall()

        for x in [0, self.w - 1]:
            for y in range(0, self.h):
                self[x, y] = Wall()

        for x in range(1, self.w - 1):
            for y in range(1, self.h - 1):
                self[x, y] = Floor()

        self.place_items()

    def place_items(self):
        cells = [cell for cell in self.data if cell and cell.walkable]
        for i in range(0, 15):
            cell = random.choice(cells)
            cells.remove(cell)
            cell.item = items.Shovel()

if __name__ == '__main__':
    import sys

    l = Dummy(30, 10)
    l.generate()

    for y in range(0, l.h):
        for x in range(0, l.w):
            cell = isinstance(l[x, y], Wall) and '*' or ' '
            sys.stdout.write(cell)
        sys.stdout.write('\n')
