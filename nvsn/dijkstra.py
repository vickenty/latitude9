import heapq

class Router (object):
    def __init__(self, owner, start, finish):
        self.owner = owner
        self.start = start
        self.finish = finish

        self.queue = [(0, start, [])]
        self.seen = set()

    def think(self, limit=50):
        while limit > 0:
            limit -= 1
            (cost, cell, path) = heapq.heappop(self.queue)
            if cell not in self.seen:
                self.seen.add(cell)
                path = path + [cell]
                if cell == self.finish:
                    return path[1:]

                for neigh in cell.neighbors():
                    if neigh not in self.seen and neigh.walkable:
                        delta = 15 if neigh.trap and neigh.trap.owner == self.owner else 1
                        heapq.heappush(self.queue, (cost + delta, neigh, path))
            
if __name__ == '__main__':
    from level import Dummy
    level = Dummy(10, 10)
    level.generate()

    router = Router(level[2, 2], level[8, 1])
    while True:
        path = router.think()
        if path:
            break

        print '.'

    print [(c.x, c.y) for c in path]

