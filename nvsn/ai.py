import random
import heapq
import player
import level

from dijkstra import Router

class AI(object):
    def __init__(self, level, player):
        self.level = level
        self.player = player
        self.visibility = player.visibility
        self.quest = player.quest

        self.target = None
        self.target_item = None
        self.router = None
        self.path = None
        self.blacklist = set()
        self.blacklist_queue = []
        self.frame = 0

    def check_goal_items(self):
        if self.target_item:
            return

        goal, cell = self.closest_goal_item()
        if goal:
            self.reset()
            self.target = cell
            self.target_item = goal

    def closest_goal_item(self):
        if not self.visibility.items:
            return None, None

        x = self.player.x
        y = self.player.y

        items = []
        items = [((c.x - x)**2 + (c.y - y)**2, c, i)
                for c, i in self.visibility.items.iteritems()
                if (i.name in self.quest.goals or random.uniform(0, 1) < 0.5) and c not in self.blacklist]

        if not items:
            return None, None

        items.sort()
        _, c, i = items[0]

        return i, c

    blacklist_time = 600

    def think(self):
        self.frame += 1

        if self.player.state:
            return

        while self.blacklist_queue and self.blacklist_queue[0][0] < self.frame:
            _, cell = heapq.heappop(self.blacklist_queue)
            self.blacklist.remove(cell)
            print 'remove', cell

        cell = self.level[self.player.x, self.player.y]

        inv = self.player.inventory
        traps = [idx for idx, item in enumerate(inv.items) if hasattr(item, 'trap_class')]

        use_prob = 0.1 if len(inv.items) < inv.size or cell._kind == level.kDoor else 0.4

        if cell.item and cell not in self.blacklist:
            if cell.item.name in self.quest.goals or random.uniform(0, 1) < 0.8:
                try:
                    self.player.pick_up()
                except player.InventoryError:
                    heapq.heappush(self.blacklist_queue, (self.frame + self.blacklist_time, cell))
                    self.blacklist.add(cell)
                    print 'blacklist', cell

        elif traps and random.uniform(0, 1) < use_prob:
            try:
                self.player.use_item(random.choice(traps))
            except player.InventoryError:
                pass

        if cell == self.target:
            self.reset()

        # Interrupt any route to get a goal item.
        self.check_goal_items()

        if not self.target and self.player.quest_done and self.visibility[self.level.exit]:
            self.target = self.level.exit

        if not self.target:
            self.target = self.find_target()

        if not self.target or self.target == cell:
            return

        if not self.router:
            self.router = Router(cell, self.target)

        if not self.path:
            try:
                self.path = self.router.think()
            except IndexError:
                self.reset()
                return

        if self.path:
            move_to = self.path.pop(0)
            dx = move_to.x - cell.x
            dy = move_to.y - cell.y
            if abs(dx) > 1 or abs(dy) > 1:
                # We're no longer on path
                self.reset()
                return
            self.player.move(dx, dy)

    def reset(self):
        self.target = self.target_item = self.router = self.path = None

    def find_target(self):
        x = self.player.x
        y = self.player.y

        tovisit = [((c.x - x)**2 + (c.y - y)**2, c) for c in self.visibility.frontier if c.walkable]

        if not tovisit:
            return random.choice(self.level.walkables)

        tovisit.sort()
        return tovisit[0][1]
