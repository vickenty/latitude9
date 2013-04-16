from __future__ import division

import pyglet
from pyglet.gl import *
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

class VisibilityUpdater (object):
    def __init__(self, level, player):
        self.level = level
        self.player = player

    def think(self):
        self.level.update_visibility(self.player.nx, self.player.ny)

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
        self.setup_render()

    def setup_level(self):
        self.level = level.Dummy(80, 50)
        self.level.generate()

    def setup_player(self):
        self.player = player.Player(self.level, 5, 5)
        self.queue.append(self.player)

        self.control = control.Keyboard(self.player, self.keys)
        self.queue.append(self.control)

    def setup_render(self):
        self.queue.append(VisibilityUpdater(self.level, self.player))

        renderer = render.LevelRenderer(self.level, self.tileset, self.batch,
                self.groups[ORDER_LEVEL],
                self.groups[ORDER_ITEMS])
        self.queue.append(renderer)

        group = self.groups[ORDER_PLAYER]
        renderer = render.PlayerRenderer(self.player, self.tileset, self.batch, group)
        self.queue.append(renderer)

    def on_draw(self):
        self.think()
        self.window.clear()
        self.setup_view()
        self.batch.draw()

        glLoadIdentity()
        self.fps.draw()

    def setup_view(self):
        w = self.window.width / 2
        h = self.window.height / 2

        px = self.player.vx * self.tileset.w
        py = self.player.vy * self.tileset.h

        maxx = self.level.w * self.tileset.w - w
        maxy = self.level.h * self.tileset.h - h

        px = min(maxx, max(w, px))
        py = min(maxy, max(h, py))

        glLoadIdentity()
        glTranslatef(
            int(w - px),
            int(h - py),
            0,
        )

    def think(self):
        [r.think() for r in self.queue]
