class Item (object):
    """Subclass this."""

    def use(self, player, level, cell):
        raise NotImplemented()

class TrapItem (Item):
    """Create a trap when used."""
    def use(self, player, level, cell):
        cell.trap = self.trap_class(player)

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
        player.freeze(self.delay)

class Shovel (TrapItem):
    name = "shovel"
    trap_class = Pit
