import pyglet
import mode
import config

import level
import render

class GameMode (mode.Mode):
    name = 'game'

    def __init__(self):
        super(GameMode, self).__init__()
        self.batch = pyglet.graphics.Batch()
        self.fps = pyglet.clock.ClockDisplay()
        self.setup_level()

    def setup_level(self):
        lev = level.Dummy(15, 15)
        lev.generate()
        tileset = render.Tileset.get_default()
        group = pyglet.graphics.OrderedGroup(0)
        self.renderer = render.LevelRenderer(lev, tileset, self.batch, group)
        self.renderer.update()

    def on_draw(self):
        self.window.clear()
        self.batch.draw()
        self.fps.draw()
