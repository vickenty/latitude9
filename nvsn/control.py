from pyglet.window import key

class Bind(object):
    def __init__(self, method, *args, **kwargs):
        self.method = method
        self.args = args
        self.kwargs = kwargs

    def __call__(self, target):
        getattr(target, self.method)(*self.args, **self.kwargs)

class Keyboard (object):
    actions = {
        key.Z: Bind('pick_up'),
        ord('1'): Bind('use_item', 0),
        ord('2'): Bind('use_item', 1),
        ord('3'): Bind('use_item', 2),
        ord('4'): Bind('use_item', 3),
        ord('5'): Bind('use_item', 4),
        ord('6'): Bind('use_item', 5),
    }

    def __init__(self, player, keys):
        self.player = player
        self.keys = keys

    def on_key_press(self, sym, mods):
        action = self.actions.get(sym)
        if action:
            action(self.player)

    def think(self):
        if self.keys[key.UP]:
            self.player.move(0, 1)
        if self.keys[key.DOWN]:
            self.player.move(0, -1)
        if self.keys[key.LEFT]:
            self.player.move(-1, 0)
        if self.keys[key.RIGHT]:
            self.player.move(1, 0)
