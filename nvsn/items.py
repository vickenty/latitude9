import sounds

class Item (object):
    """Subclass this."""

    def use(self, player, level, cell):
        raise NotImplemented()

class TrapItem (Item):
    """Create a trap when used."""
    def use(self, player, level, cell):
        self.on_use()
        cell.trap = self.trap_class(player)

class GoalItem (Item):
    """Droppable item."""

    types = ['gem%d' % (seq,) for seq in range(1, 7)]

    def __init__(self, name):
        self.name = name

    def use(self, player, level, cell):
        cell.item = self

class Trap (object):
    """Subclass this."""
    def __init__(self, owner):
        self.owner = owner

    def affect(self, player):
        raise NotImplemented()

class Pit (Trap):
    name = 'pit'
    delay = 120

    def affect(self, player):
        sounds.play('fall')
        player.freeze(self.delay)

class Mine (Trap):
    name = 'mine'

    def affect(self, player):
        sounds.play('explosion')
        player.die()

class Shovel (TrapItem):
    name = "shovel"
    trap_class = Pit

    def on_use(self):
        sounds.play('dig')

class MineKit (TrapItem):
    name = 'minekit'
    trap_class = Mine

    def on_use(self):
        sounds.play('mine')
