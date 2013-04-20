import random
import items

kVoid, kWall, kRoom, kDoor, kExit = constants = [0] + [1 << i for i in range(4)]
kWalkable = kRoom | kDoor | kExit
kCellNames = {kVoid: 'void', kWall: 'wall', kRoom: 'floor', kDoor: 'floor', kExit: 'exit'}

class Cell(object):
    HIDDEN = 0
    MEMORY = 1
    LIT = 2

    _dungeon = None
    _pos = None
    _kind = None
    _room = None
    item = None
    trap = None
    _neighbors = None

    def __init__(self, dungeon, pos, kind = kVoid, room = None):
        super(Cell, self).__init__()

        self._dungeon = dungeon
        self._pos = tuple(pos)
        self.x, self.y = self._pos
        self._kind = kVoid
        self._room = room

    def __str__(self):
        return "<Cell %s, 0x%02x, %s>" % (self._pos, self._kind, self._room)

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return self._pos.__hash__()

    def __eq__(self, b):
        if not b:
            return False
        return self._pos.__eq__(b._pos)

    def __cmp__(self, b):
        v = cmp(self._pos[0], b._pos[0])
        if v == 0:
            v = cmp(self._pos[1], b._pos[1])
        return v

    def name(self):
        return kCellNames.get(self._kind, "cell-%02x" % self._kind)

    def walkable(self):
        return self._kind & kWalkable > 0

    def enter(self, player):
        if self.trap:
            self.trap.affect(player)
            self.trap = None

        if self._kind == kExit and player.quest_done:
            player.win()

    def neighbors(self):
        if self._neighbors is None:
            self._neighbors = set()

            for dx, dy in [(0,1), (0, -1), (1,0), (-1,0)]:
                c = self._dungeon.cell(self._pos[0] + dx, self._pos[1] + dy)
                if c is not None:
                    self._neighbors.add(c)
        return self._neighbors

    def neighborsOfKind(self, kind):
        count = 0

        for c in self.neighbors():
            if c.kind() == kind:
                count += 1

        return count

    def distanceTo(self, b):
        #return math.sqrt(pow(self._pos[0] - b._pos[0], 2) + pow(self._pos[1] - b._pos[1], 2))
        return abs(self._pos[0] - b._pos[0]) + abs(self._pos[1] - b._pos[1])

    def kind(self):
        return self._kind

    def room(self):
        return self._room

    def pos(self):
        return self._pos

    def update(self, kind = None, room = None, **kw):
        oldKind = self._kind
        if kind is not None:
            self._kind = kind

        # I know this means the method can't clear room. I don't need it.
        if room is not None:
            self._room = room

        if self._room is not None and self._kind != oldKind:
            if oldKind is kWall:
                self._room.removeFromWalls(self)
            elif self._kind == kWall:
                self._room.addToWalls(self)

        if "trap" in kw: self.trap = kw["trap"]
        if "item" in kw: self.item = kw["item"]

class Visibility (dict):
    def __init__(self, level, default=Cell.HIDDEN):
        super(Visibility, self).__init__()
        self.level = level
        self.w = level.w
        self.h = level.h
        self.frontier = set()
        self.update(dict((cell, default) for cell in level.data()))
        self.dirty_list = self.keys()
        self.items = {}

    def update_visibility(self, cx, cy, radius=6.5, cansee=True):
        r2 = radius**2
        for x in clamped_range(cx, radius, 0, self.w):
            for y in clamped_range(cy, radius, 0, self.h):
                cell = self.level[x, y]
                d2 = (x - cx)**2 + (y - cy)**2
                if cell:
                    if d2 <= r2:
                        self[cell] = cell.LIT if cansee else cell.MEMORY
                        self.update_frontier(cell)
                        if cell.item:
                            self.items[cell] = cell.item
                        elif cell in self.items:
                            del self.items[cell]
                    else:
                        self[cell] = self[cell] and cell.MEMORY
                        if cell in self.items:
                            del self.items[cell]

                    self.dirty_list.append(cell)

    def update_frontier(self, cell):
        front = any(self[n] == cell.HIDDEN for n in cell.neighbors())
        if front:
            self.frontier.add(cell)
        elif cell in self.frontier:
            self.frontier.remove(cell)

    def wipe(self):
        self.dirty_list = []

def clamped_range(center, delta, minv, maxv):
    delta = int(delta + 0.5)
    return xrange(max(minv, center - delta), min(maxv, center + delta + 1))

class Level (object):
    def __init__(self, w, h):
        self.w = w
        self.h = h

    def __getitem__(self, key):
        return None

    def data(self):
        return None

    def offset(self, x, y):
        return y * self.w + x

#class Dummy (Level):
#    def __init__(self, w, h):
#        super(Dummy, self).__init__(w, h)
#
#    def generate(self):
#        for y in [0, self.h - 1]:
#            for x in range(0, self.w):
#                self[x, y] = Wall()
#
#        for x in [0, self.w - 1]:
#            for y in range(0, self.h):
#                self[x, y] = Wall()
#
#        for y in range(1, self.h - 5):
#            self[self.w // 2, y] = Wall()
#
#        for x in range(1, self.w - 1):
#            for y in range(1, self.h - 1):
#                if not self[x, y]:
#                    if x > self.w * 0.75 and y > self.h * 0.75:
#                        tile = ExitArea
#                    else:
#                        tile = Floor
#                    self[x, y] = tile()
#
#                    if tile == ExitArea:
#                        self.exit = self[x, y]
#
#        self.place_items()
#        self.build_graph()
#
#    def place_items(self):
#        cells = [cell for cell in self.data if cell and cell.walkable]
#        arsenal = [items.Shovel, items.MineKit]
#        for i in range(0, 15):
#            cell = random.choice(cells)
#            cells.remove(cell)
#            cell.item = random.choice(arsenal)()
#
#        for kind in items.GoalItem.types:
#            cell = random.choice(cells)
#            cells.remove(cell)
#            cell.item = items.GoalItem(kind)
#
#    def build_graph(self):
#        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
#
#        for cell in self.data:
#            if not cell:
#                continue
#
#            for dx, dy in directions:
#                x = cell.x + dx
#                y = cell.y + dy
#                if 0 <= x < self.w and 0 <= y < self.h:
#                    neigh = self[cell.x + dx, cell.y + dy]
#                    cell.neighbors.append(neigh)
#
#if __name__ == '__main__':
#    import sys
#
#    l = Dummy(30, 10)
#    l.generate()
#
#    for y in range(0, l.h):
#        for x in range(0, l.w):
#            cell = isinstance(l[x, y], Wall) and '*' or ' '
#            sys.stdout.write(cell)
#        sys.stdout.write('\n')
