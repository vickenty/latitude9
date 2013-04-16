from pyglet.window import key

class Keyboard (object):
    def __init__(self, player, keys):
        self.player = player
        self.keys = keys

    def on_key_press(self, sym, mods):
        if sym == key.Z:
            self.player.pick_up()

    def think(self):
        if self.keys[key.UP]:
            self.player.move(0, 1)
        if self.keys[key.DOWN]:
            self.player.move(0, -1)
        if self.keys[key.LEFT]:
            self.player.move(-1, 0)
        if self.keys[key.RIGHT]:
            self.player.move(1, 0)
