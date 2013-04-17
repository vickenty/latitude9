class Item (object):
    """Subclass this."""
    name = 'item'

    def use(self, player, level, cell):
        cell.trap = Trap(player)
        level.dirty_list.append(cell)

class Trap (object):
    """Subclass this."""
    name = 'trap'

    delay = 120

    def __init__(self, owner):
        self.owner = owner

    def affect(self, player):
        player.freeze(self.delay)
