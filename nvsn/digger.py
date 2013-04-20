from random import randint, choice

def vadd(v1, v2):
    return v1[0] + v2[0], v1[1] + v2[1]

def vsub(v1, v2):
    return v1[0] - v2[0], v1[1] - v2[1]

def vmul(v1, v2):
    return v1[0] * v2[0], v1[1] * v2[1]

def vmin(v1, v2):
    return min(v1[0], v2[0]), min(v1[1], v2[1])

def vmax(v1, v2):
    return max(v1[0], v2[0]), max(v1[1], v2[1])

def randvect(unit, minlen, maxlen):
    return randint(minlen, maxlen) * unit[0], randint(minlen, maxlen) * unit[1]


directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

class Feature(object):
    def __init__(self, p1, p2, is_room=False):
        self.p1 = p1
        self.p2 = p2
        self.is_room = is_room

    def overlap(self, other):
        return self.inside(other.p1) or self.inside(other.p2)
    
    def inside(self, p):
        return self.p1[0] <= p[0] <= self.p2[0] and self.p1[1] <= p[1] <= self.p2[0]
    
    def get_wall(self, side):
        if side[0] == -1:
            return self.p1, (0, 1), self.p2[1] - self.p1[1]
        if side[0] == 1:
            return (self.p2[0], self.p1[1]), (0, 1), self.p2[1] - self.p1[1]
        if side[1] == -1:
            return self.p1, (1, 0), self.p2[0] - self.p1[0]
        if side[1] == 1:
            return (self.p1[0], self.p2[1]), (1, 0), self.p2[0] - self.p1[0]

    def rand_pos(self, side):
        pos, direction, length = self.get_wall(side)
        return vadd(pos, randvect(direction, 1, length))

class Digger(object):
    min_room = 3
    max_room = 5
    min_doors = 2
    max_doors = 4
    min_corridor = 2
    max_corridor = 4
    max_features = 15

    def __init__(self):
        self.features = []
        self.doors = []

    def build(self):
        self.add_room((0, 0), (0, 1))

        while self.doors:
            door = choice(self.doors)
            self.doors.remove(door)
            
            pos, direction, kind = door
            if kind == 'room':
                self.add_corridor(pos, direction)
            else:
                self.add_room(pos, direction)

    def add_room(self, pos, direction):
        size = randvect((1, 1), self.min_room, self.max_room)
        far_end = vadd(pos, vmul(direction, size))

        if far_end[0] == pos[0]:
            far_end = randint(pos[0] - size[0], pos[0] + size[0]), far_end[1]
            if far_end[0] > pos[0]:
                other = far_end[0] - size[0], pos[1]
            else:
                other = far_end[0] + size[0], pos[1]

        if far_end[1] == pos[1]:
            far_end = far_end[0], randint(pos[1] - size[1], pos[1] + size[1])
            if far_end[1] > pos[1]:
                other = pos[0], far_end[1] - size[1]
            else:
                other = pos[0], far_end[1] + size[1]

        p1 = vmin(far_end, other)
        p2 = vmax(far_end, other)

        assert p2[0] - p1[0] == size[0]
        assert p2[1] - p1[1] == size[1]

        room = Feature(p1, p2, True)
        self.features.append(room)

        if len(self.features) < self.max_features:
            ndoors = randint(self.min_doors, self.max_doors)
        else:
            ndoors = 0

        for _ in range(ndoors):
            side = choice(directions)
            door = room.rand_pos(side)
            if door in self.doors:
                continue
            self.doors.append((door, side, 'room'))

    def add_corridor(self, pos, direction):
        size = randvect(direction, self.min_corridor, self.max_corridor)
        end = vadd(pos, size)

        corridor = Feature(vmin(pos, end), vmax(pos, end), 'corridor')
        self.features.append(corridor)
        self.doors.append((end, direction, 'corridor'))

    def carve(self):
        p1 = reduce(vmin, (f.p1 for f in self.features), (0, 0))
        p2 = reduce(vmax, (f.p2 for f in self.features), (0, 0))
        data = {}

        for feature in self.features:
            for x in range(feature.p1[0], feature.p2[0] + 1):
                for y in range(feature.p1[1], feature.p2[1] + 1):
                    pos = vadd((1, 1), vsub((x, y), p1))
                    data[pos] = 1

        return data, vadd(vsub(p2, p1), (2, 2))

if __name__ == '__main__':
    import sys
    d = Digger()
    d.build()
    data, size = d.carve()
    print size
    for y in range(0, size[1]):
        for x in range(0, size[0]):
            if data.get((x, y)):
                sys.stdout.write('.')
            else:
                sys.stdout.write(' ')
        sys.stdout.write('\n')
