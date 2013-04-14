class Cell (object):
    __slots__ = ['x', 'y', 'visible']

    def __init__(self, x=0, y=0, visible=True):
        self.x = x
        self.y = y
        self.visible = visible

class Wall(Cell):
    name = 'wall'

class Floor(Cell):
    name = 'floor'

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

if __name__ == '__main__':
    import sys

    l = Dummy(30, 10)
    l.generate()

    for y in range(0, l.h):
        for x in range(0, l.w):
            cell = l[x, y] and '*' or ' '
            sys.stdout.write(cell)
        sys.stdout.write('\n')
