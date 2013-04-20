from __future__ import division
import random
from math import sqrt
import sounds

import level

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
        self.reset()

    def reset(self):
        self.items = [None] * self.size

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
    death_delay = 16
    respawn_delay = 64

    IDLE = 0
    MOVING = 1
    DIE = 2
    RESPAWN = 3
    TRAPPED = 4

    def __init__(self, level, visibility, quest, x, y):
        self.level = level
        self.visibility = visibility
        self.quest = quest
        self.x = x
        self.y = y
        self.init_pos = x, y
        self.inventory = Inventory()
        self.wait = 0
        self.nx = self.vx = self.x
        self.ny = self.vy = self.y
        self.dx = 0
        self.dy = 0
        self.won = False
        self.quest_done = False
        self.alive = True
        self.state = self.IDLE

    def move(self, dx, dy):
        if self.state:
            return

        nx = self.x + dx
        ny = self.y + dy

        if self.level[nx, ny].walkable():
            self.state = self.MOVING

            # delta, used to animate movement
            self.dx = dx
            self.dy = dy
            # new pos
            self.nx = nx
            self.ny = ny

            self.animate(self.walk_delay)

    def animate(self, delay):
        self.wait = self.anim_delay = delay

    def pick_up(self):
        if self.wait > 0:
            return

        cell = self.level[self.x, self.y]

        if not cell.item:
            raise NothingHere()

        item = cell.item
        self.inventory.add(item)
        cell.item = None

        if item.name in self.quest.goals:
            sounds.play('goal')
        else:
            sounds.play('pick')

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
        self.update_visibility()

        if self.wait > 0:
            self.wait -= 1

            d = 1 - self.wait / self.anim_delay
            self.vx = self.x + d * self.dx
            self.vy = self.y + d * self.dy

        if not self.wait and (self.dx or self.dy):
            self.x = self.vx = self.nx
            self.y = self.vy = self.ny
            self.dx = 0
            self.dy = 0
            self.alive = True
            self.level[self.x, self.y].enter(self)

        if not self.wait and self.state:
            self.state = self.IDLE

    def update_visibility(self):
        self.visibility.update_visibility(self.nx, self.ny, cansee=self.alive)

    def freeze(self, time):
        self.state = self.TRAPPED
        self.wait = time

    def win(self):
        self.won = True

    def die(self):
        self.state = self.DIE
        self.alive = False

        self.update_visibility()
        self.scatter_items()
        self.inventory.reset()

        self.nx, self.ny = self.init_pos
        self.dx = self.nx - self.x
        self.dy = self.ny - self.y
        self.animate(self.walk_delay * int(sqrt(self.dx**2 + self.dy**2)))

    def scatter_items(self):
        items = self.inventory.items[:]
        radius = 0

        while items:
            radius += 1
            cells = list(self.find_free_cells(radius))
            if not cells:
                radius += 1
                continue

            while items and cells:
                cell = random.choice(cells)
                cells.remove(cell)
                cell.item = items.pop()

    def find_free_cells(self, radius):
        for x in level.clamped_range(self.x, radius, 0, self.level.w):
            for y in level.clamped_range(self.y, radius, 0, self.level.h):
                cell = self.level[x, y]
                if cell.walkable() and not (cell.item or cell.trap):
                    yield cell
