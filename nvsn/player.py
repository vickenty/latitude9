from __future__ import division

class InventoryError (Exception):
    pass

class InventoryFull (InventoryError):
    '''Inventory full'''

class NothingHere (InventoryError):
    '''Nothing here to pick up'''

class Inventory (object):
    size = 6
    def __init__(self):
        self.items = [None] * self.size
        self.active = 0

    def add(self, item):
        for idx, slot in enumerate(self.items):
            if slot is None:
                self.items[idx] = item
                return

        raise InventoryFull()

    def select(self, idx):
        self.active = idx

class Player (object):
    walk_delay = 8

    def __init__(self, level, x, y):
        self.level = level
        self.x = x
        self.y = y
        self.inventory = Inventory()
        self.wait = 0
        self.nx = self.vx = self.x
        self.ny = self.vy = self.y
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

    def pick_up(self):
        if self.wait > 0:
            return

        cell = self.level[self.x, self.y]

        if not cell.item:
            raise NothingHere()

        self.inventory.add(cell.item)
        cell.item = None

        print self.inventory.items

    def think(self):
        if self.wait > 0:
            self.wait -= 1

            d = 1 - self.wait / self.walk_delay
            self.vx = self.x + d * self.dx
            self.vy = self.y + d * self.dy

        if not self.wait:
            self.x = self.vx = self.nx
            self.y = self.vy = self.ny
            self.dx = 0
            self.dy = 0

