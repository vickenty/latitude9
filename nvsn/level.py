class Wall (object):
    pass

class Level (object):
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.data = [None] * self.w * self.h

    def at(self, x, y):
        return self.data[self.offset(x, y)]

    def set(self, x, y, tile):
        self.data[self.offset(x, y)] = tile

    def offset(self, x, y):
        return y * self.w + x

class Dummy (Level):
    wall = Wall()

    def __init__(self, w, h):
        super(Dummy, self).__init__(w, h)

    def generate(self):
        for y in [0, self.h - 1]:
            for x in range(0, self.w):
                self.set(x, y, self.wall)

        for x in [0, self.w - 1]:
            for y in range(0, self.h):
                self.set(x, y, self.wall)

if __name__ == '__main__':
    import sys

    l = Dummy(30, 10)
    l.generate()

    for y in range(0, l.h):
        for x in range(0, l.w):
            tile = l.at(x, y) and '*' or ' '
            sys.stdout.write(tile)
        sys.stdout.write('\n')
