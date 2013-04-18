from __future__ import division

class InventoryError (Exception):
    pass

class InventoryFull (InventoryError):
    '''Inventory full'''

class NothingHere (InventoryError):
    '''Nothing here to pick up'''

class SlotEmpty (InventoryError):
    '''Empty slot'''

class SpaceUsed (InventoryError):
    '''There's already something here.'''

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

    def get(self, slot):
        item = self.items[slot]
        if item:
            self.items[slot] = None
            return item
        else:
            raise SlotEmpty()

    def item_types(self):
        return set(i.name for i in self.items if i)

class Player (object):
    walk_delay = 8

    def __init__(self, level, quest, x, y):
        self.level = level
        self.quest = quest
        self.x = x
        self.y = y
        self.inventory = Inventory()
        self.wait = 0
        self.nx = self.vx = self.x
        self.ny = self.vy = self.y
        self.dx = 0
        self.dy = 0
        self.won = False

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

        self.update_quest_status()

    def use_item(self, slot):
        cell = self.level[self.x, self.y]

        if cell.item or cell.trap:
            raise SpaceUsed()

        item = self.inventory.get(slot)
        item.use(self, self.level, cell)

        self.update_quest_status()

    def update_quest_status(self):
        has = self.inventory.item_types()
        self.quest_done = all(goal in has for goal in self.quest.goals)

    def think(self):
        if self.wait > 0:
            self.wait -= 1

            d = 1 - self.wait / self.walk_delay
            self.vx = self.x + d * self.dx
            self.vy = self.y + d * self.dy

        if not self.wait and (self.dx or self.dy):
            self.x = self.vx = self.nx
            self.y = self.vy = self.ny
            self.dx = 0
            self.dy = 0

            self.level[self.x, self.y].enter(self)

    def freeze(self, time):
        self.wait = time

    def win(self):
        self.won = True

    def die(self):
        pass
