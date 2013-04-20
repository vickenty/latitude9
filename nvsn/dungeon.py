import random, collections, math
import level, items

kVoid, kWall, kRoom, kDoor, kExit = level.constants
kFancy = collections.defaultdict(lambda: "?", {kVoid: ' ', kWall: '#', kRoom: '.', kDoor: 'D', kExit: 'E'})

def _centeredBounds(center, size):
    halfSize = size / 2
    return (center - halfSize, center + halfSize + size % 2)

class Room(object):
    _id = None
    _size = None
    _connections = None
    _cells = None
    _walls = None
    _bounds = None
    _dungeon = None

    def __init__(self, id, xBounds, yBounds, dungeon):
        super(Room, self).__init__()

        self._id = id
        self._connections = set()
        self._cells = set()
        self._walls = set()
        self._bounds = [list(xBounds), list(yBounds)]
        self._size = [self._bounds[0][1] - self._bounds[0][0],
                      self._bounds[1][1] - self._bounds[1][0]]
        self._dungeon = dungeon

    def __eq__(self, b):
        return self._id == b._id

    def cells(self):
        return self._cells

    def claimCells(self):
        success = True
        room = self
        edgeRow = [kWall] * (self._size[0])
        normalRow = [kWall] + [kRoom] * (self._size[0] - 2) + [kWall]
        yRange = range(*self._bounds[1])

        for y in yRange:
            if y == yRange[0] or y == yRange[-1]:
                row = edgeRow
            else:
                row = normalRow

            for dx in range(self._size[0]):
                c = self._dungeon.cell(self._bounds[0][0] + dx, y)
                if c.kind() == kRoom or c.kind() == kWall:
                    if room != c.room():
                        c.room().absorb(room)
                        success = False
                        room._dungeon.removeRoom(room)
                        room = c.room()

                    newKind = row[dx]
                    if c.kind() == kRoom or newKind == kRoom:
                        newKind = kRoom
                    c.update(kind = newKind)
                else:
                    c.update(kind = row[dx], room = room)
                    room._cells.add(c)

        return success

    def addToWalls(self, cell):
        self._walls.add(cell)

    def removeFromWalls(self, cell):
        self._walls.discard(cell)

    def tidy(self):
        left, right, up, down = (-1, 0), (1, 0), (0, -1), (0, 1)
        for c in sorted(self._cells):
            if c.kind() == kWall:
                for (o1, o2, o3, o4) in [(left, right, up, down), (up, down, left, right)]:
                    c1 = self._dungeon.cell(c._pos[0] + o1[0], c._pos[1] + o1[1])
                    c2 = self._dungeon.cell(c._pos[0] + o2[0], c._pos[1] + o2[1])

                    if c1 is not None and c2 is not None and c1.kind() == c2.kind() == kRoom:
                        c3 = self._dungeon.cell(c._pos[0] + o3[0], c._pos[1] + o3[1])
                        c4 = self._dungeon.cell(c._pos[0] + o4[0], c._pos[1] + o4[1])

                        # We want wall on both sides of our door, why
                        # would you have a door otherwise?
                        if c3 is not None and c3.kind() == kWall and \
                           c4 is not None and c4.kind() == kWall:
                            c.update(kind=kDoor)

    def connected(self):
        return len(self._connections) > 0

    def connect(self, room):
        self._connections.add(room)
        room._connections.add(self)

    def disconnect(self, room):
        self._connections.discard(room)
        room._connections.discard(self)

    def buildCorridorTo(self, target, cells = None):
        if cells is None:
            cells = self.closestCells(target)
        room = cells[0].room()
        pos = list(cells[0].pos())
        dx = cells[1].pos()[0] - cells[0].pos()[0]
        dy = cells[1].pos()[1] - cells[0].pos()[1]
        cellsBeforeSwitch = (abs(dx) + abs(dy)) / 2

        self.connect(target)

        c1, c2 = self._dungeon.cell(pos[0] - 1, pos[1]), self._dungeon.cell(pos[0] + 1, pos[1])
        if (c1 is not None and c1.kind() == kWall) or (c2 is not None and c2.kind() == kWall):
            room, cellsBeforeSwitch = self._buildCorridor(cells, dy, pos, 1, room, cellsBeforeSwitch, 0)
            if abs(dx) > 0 and abs(dy) > 0:
                self._buildBend(pos, dx, dy, room, 1)
            room, cellsBeforeSwitch = self._buildCorridor(cells, dx, pos, 0, room, cellsBeforeSwitch, int(abs(dy) > 0))
        else:
            room, cellsBeforeSwitch = self._buildCorridor(cells, dx, pos, 0, room, cellsBeforeSwitch, 0)
            if abs(dx) > 0 and abs(dy) > 0:
                self._buildBend(pos, dx, dy, room, -1)
            room, cellsBeforeSwitch = self._buildCorridor(cells, dy, pos, 1, room, cellsBeforeSwitch, int(abs(dx) > 0))

    def _buildBend(self, pos, dx, dy, room, ddSign):
        ddx = ddSign * abs(dx) / dx
        ddy = ddSign * abs(dy) / dy

        self._dungeon.cell(pos[0] - ddx, pos[1]    ).update(kind = kWall, room = room)
        self._dungeon.cell(pos[0],       pos[1] + ddy).update(kind = kWall, room = room)
        self._dungeon.cell(pos[0] - ddx, pos[1] + ddy).update(kind = kWall, room = room)

        self._dungeon.cell(*pos).update(kind = kRoom, room = room)

    def _buildCorridor(self, cells, delta, pos, pIndex, room, cellsBeforeSwitch, startDelta):
        if abs(delta) > 0:
            dir = abs(delta) / delta
            delta = abs(delta) - startDelta
            sideIndex = int(not pIndex)

            pos[pIndex] += dir * startDelta

            while delta >= 0:
                kind = kRoom
                if cellsBeforeSwitch == 0:
                    room = cells[1].room()
                    kind = kDoor

                c = self._dungeon.cell(*pos)
                if c.room() is None:
                    for sideDelta in (-1, 1):
                        p2 = list(pos)
                        p2[sideIndex] += sideDelta
                        c1 = self._dungeon.cell(*p2)

                        if c1 is not None:
                            c1.update(kind = kWall, room = room)

                c.update(kind = kind, room = room)

                cellsBeforeSwitch -= 1
                delta -= 1
                pos[pIndex] += dir
        return room, cellsBeforeSwitch

    def bounds(self):
        return (tuple(self._bounds[0]), tuple(self._bounds[1]))

    def absorb(self, room):
        for c in room._cells:
            self._cells.add(c)
            c.update(room = self)
        room._cells.clear()

        self._walls.update(room._walls)
        room._walls.clear()

        for r in room._connections:
            self.connect(r2)
            room.disconnect(r2)

    def canReachRoom(self, target):
        return self._canReachRoom(target, set())

    def _canReachRoom(self, target, visited):
        visited.add(self)
        if target == self:
            return True

        for r in self._connections:
            if r not in visited and r._canReachRoom(target, visited):
                return True

        return False

    def closestCells(self, target):
        c1 = c2 = None
        d = None
        for w1 in self._walls:
            if w1.neighborsOfKind(kVoid) == 1:
                for w2 in target._walls:
                    if w2.neighborsOfKind(kVoid) == 1:
                        d1 = w1.distanceTo(w2)
                        if d is None or d1 < d:
                            d = d1
                            c1 = w1
                            c2 = w2
        return c1, c2

    def distanceTo(self, target):
        c1,c2 = self.closestCells(target)

        return c1.distanceTo(c2)

    def __str__(self):
        return "<Room #%s>" % (self._id)

    def __repr__(self):
        return self.__str__()

class Dungeon(level.Level):
    _minSize = 5
    _maxSize = 10
    _chamberMinSize = 8
    _chamberMaxSize = 12
    _targetRatio = 0.5

    _random = None
    _dungeon = None
    _seed = None
    _width = _height = None
    _chamber = None
    _rooms = None
    _nextRoomId = 0


    def __init__(self, width, height, seed = None, **kw):
        super(Dungeon, self).__init__(width, height)

        self._width = int(width)
        self._height = int(height)

        self._dungeon = map(lambda y: map(lambda x: level.Cell(self, (x,y)), range(self._width)), range(self._height))
        self._rooms = set()

        if seed is None:
            self._seed = random.randint(0, (1 << 32) - 1)
        else:
            self._seed = long(seed)
        self._random = random.Random(self._seed)

        for k,v in kw.items():
            if hasattr(self, "_%s" % k):
                if type(v) is type(getattr(self, "_%s" % k)):
                    setattr(self, "_%s" % k, v)

    def __getitem__(self, key):
        return self.cell(*key)

    def __setitem__(self, key, cell):
        raise Exception("Don't set cells like that - do d.cell(x,y).update(blargh)")

    def _fillRatio(self):
        filledCells = sum(
            map(lambda a: len(a),
                [filter(lambda c: c.kind() != kVoid, r) for r in self._dungeon]),
            0.0)

        return float(filledCells) / (self._width * self._height)

    def data(self):
        data = []
        for row in self._dungeon:
            data += row
        return data

    def generate(self):
        pos, size = self._findSpot(self._chamberMinSize, self._chamberMaxSize)
        self._chamber = self._addRoom(pos, size)

        while self._fillRatio() < self._targetRatio:
            pos, size = self._findSpot(self._minSize, self._maxSize)
            self._addRoom(pos, size)

        for r in self._rooms:
            r.tidy()

        self._buildCorridors()
        self._placeExit()
        self._placeItems()
        #self.dump()

    def _buildCorridors(self):
        if len(self._rooms) > 1:
            reachables = set(filter(lambda r: r.canReachRoom(self._chamber), self._rooms))
            unreachables = set(filter(lambda r: not r.canReachRoom(self._chamber), self._rooms))
            src, dst = self._findUnreachableRoom(reachables, unreachables)

            while src is not None:
                src.buildCorridorTo(dst)
                reachables.add(src)
                unreachables.remove(src)
                src, dst = self._findUnreachableRoom(reachables, unreachables)

    def _placeExit(self):
        chamberCells = filter(lambda c: c.kind() == kRoom, self._chamber.cells())
        return self._random.choice(chamberCells)

    def spawnPoint(self):
        possibleCells = filter(lambda c: c.kind() == kRoom, self.data())

        return random.choice(possibleCells).pos()

    def _placeItems(self):
        possibleCells = filter(lambda c: c.kind() == kRoom, self.data())
        arsenal = [items.Shovel, items.MineKit]

        for i in range(15):
            c = random.choice(possibleCells)
            possibleCells.remove(c)
            c.update(item = random.choice(arsenal)())

        for kind in items.GoalItem.types:
            c = random.choice(possibleCells)
            possibleCells.remove(c)
            c.update(item = items.GoalItem(kind))

    def _findUnreachableRoom(self, reachables, unreachables):
        d = None
        src = dst = None

        for r in unreachables:
            if not r.canReachRoom(self._chamber):
                for r2 in reachables:
                    d1 = r.distanceTo(r2)
                    if d is None or d1 < d:
                        d = d1
                        src = r
                        dst = r2
        return src, dst

    def _findSpot(self, minSize, maxSize):
        def _genPosAndSize():
            size = (self._random.randint(minSize, maxSize),
                    self._random.randint(minSize, maxSize))
            pos = (self._random.randint(size[0] / 2, self._width  - size[0] / 2 - size[0] % 2),
                   self._random.randint(size[1] / 2, self._height - size[1] / 2 - size[1] % 2))

            return pos, size

        # loop over this and check with _roomInRect != None to avoid overlaps
        pos, size = _genPosAndSize()

        return pos, size

    def _addRoom(self, pos, size):
        xBounds = _centeredBounds(pos[0], size[0])
        yBounds = _centeredBounds(pos[1], size[1])

        room = Room(self._nextRoomId, xBounds, yBounds, self)
        if room.claimCells():
            self._nextRoomId += 1
            self._rooms.add(room)
        else:
            room = None

        return room

    def cell(self, x, y):
        if (0 <= x and x < self._width) and (0 <= y and y < self._height):
            return self._dungeon[y][x]
        else:
            return None

    def __getitem__(self, key):
        return self.cell(*key)

    def removeRoom(self, room):
        self._rooms.discard(room)

    def dump(self, fancy = True):
        def _fancy(c):
            if c.kind() == kRoom:
                if c.room().connected(): return kFancy[kRoom]
                else: return str(c.room()._id % 10)
            #elif c.kind() == kWall:
            #    return str(c.neighborsOfKind(kVoid))
            else:
                return kFancy[c.kind()]

        print "Dungeon #%i" % self._seed
        print "w: %i, h: %i" % (self._width, self._height)
        print "fill: %s" % self._fillRatio()
        print "rooms: %s" % self._rooms

        f = lambda c: str(c[0])
        if fancy:
            f = _fancy
        for y in range(len(self._dungeon)):
            print "".join([f(self._dungeon[y][x]) for x in range(len(self._dungeon[y]))])

def main():
    dungeon = Dungeon(50, 50, targetRatio = 0.25, seed = None)#, seed=3734095578)#, seed = 4026426881)
    dungeon.dump()

if __name__ == "__main__":
    main()
