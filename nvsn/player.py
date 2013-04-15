class InventoryFull (Exception):
    pass

class Inventory (object):
    size = 6
    def __init__(self):
        self.items = [None] * self.size
        self.active = 0

    def add(self, item):
        for i, item in enumerate(self.items):
            if item is None:
                self.items[i] = item
                return i

        raise InventoryFull()

    def select(self, idx):
        self.active = idx

class Player (object):
    walk_delay = 12

    def __init__(self, level, x, y):
        self.level = level
        self.x = x
        self.y = y
        self.inventory = Inventory()
        self.wait = 0
        self.nx = self.x
        self.ny = self.y
        self.dx = 0
        self.dy = 0

    def move(self, dx, dy):
        if self.wait > 0:
            return

        nx = self.x + dx
        ny = self.y + dy

        if self.level[nx, ny].walkable:
            # delta, used to animate movement
            self.dx = dx
            self.dy = dy
            # new pos
            self.nx = nx
            self.ny = ny

            self.wait = self.walk_delay

    def think(self):
        if self.wait > 0:
            self.wait -= 1

        if not self.wait:
            self.x = self.nx
            self.y = self.ny
            self.dx = 0
            self.dy = 0

