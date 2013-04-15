import pyglet
import mode
import config

import level
import render
import player
import control

ORDER_LEVEL = 0
ORDER_ITEMS = 1
ORDER_PLAYER = 2
ORDER_EFFECT = 3
ORDER_TOP = 4

class GameMode (mode.Mode):
    name = 'game'

    def __init__(self):
        super(GameMode, self).__init__()

        self.batch = pyglet.graphics.Batch()
        self.groups = [pyglet.graphics.OrderedGroup(o) for o in range(ORDER_TOP)]

        self.fps = pyglet.clock.ClockDisplay()

        self.queue = []

        self.tileset = render.Tileset.get_default()

        self.setup_level()
        self.setup_player()

    def setup_level(self):
        self.level = level.Dummy(15, 15)
        self.level.generate()

        group = self.groups[ORDER_LEVEL]
        renderer = render.LevelRenderer(self.level, self.tileset, self.batch, group)
        self.queue.append(renderer)

    def setup_player(self):
        self.player = player.Player(self.level, 5, 5)
        self.queue.append(self.player)

        self.control = control.Keyboard(self.player, self.keys)
        self.queue.append(self.control)

        group = self.groups[ORDER_PLAYER]
        renderer = render.PlayerRenderer(self.player, self.tileset, self.batch, group)
        self.queue.append(renderer)

    def on_draw(self):
        self.think()
        self.window.clear()
        self.batch.draw()
        self.fps.draw()

    def think(self):
        [r.think() for r in self.queue]
