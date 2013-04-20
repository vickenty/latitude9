from __future__ import division

import pyglet
from pyglet.gl import *
import mode
import config

import level
import dungeon
import render
import player
import control
import quest

ORDER_LEVEL = 0
ORDER_ITEMS = 1
ORDER_PLAYER = 2
ORDER_TOP = 3

class GameMode (mode.Mode):
    name = 'game'
    volume = 0.7

    def __init__(self):
        super(GameMode, self).__init__()

        self.scroll_batch = pyglet.graphics.Batch()
        self.static_batch = pyglet.graphics.Batch()

        self.groups = [pyglet.graphics.OrderedGroup(o) for o in range(ORDER_TOP)]

        self.fps = pyglet.clock.ClockDisplay()

        self.queue = []

        self.tileset = render.Tileset.get_default()

        self.setup_level()
        self.setup_player()
        self.setup_render()
        self.setup_music()

    def setup_level(self):
        self.level = dungeon.Dungeon(80, 50, targetRatio = 0.25)
        self.level.generate()

        self.quest = quest.Quest.new_random()

    def setup_player(self):
        visibility = level.Visibility(self.level)
        spawnPoint = self.level.spawnPoint()

        self.player = player.Player(self.level, visibility, self.quest, spawnPoint[0], spawnPoint[1])
        self.queue.append(self.player)

        self.control = control.Keyboard(self.player, self.keys)

    def on_key_press(self, sym, mods):
        if sym == pyglet.window.key.P:
            self.app.switch_handler('pause', self.music_player, suspend=True)
        self.safe_call(self.control.on_key_press, sym, mods)

    def setup_render(self):
        renderer = render.LevelRenderer(
                self.player,
                self.level,
                self.tileset,
                self.scroll_batch,
                self.groups[ORDER_LEVEL],
                self.groups[ORDER_ITEMS])
        self.queue.append(renderer)

        group = self.groups[ORDER_PLAYER]
        renderer = render.PlayerRenderer(
                self.player,
                self.tileset,
                self.scroll_batch,
                self.groups[ORDER_PLAYER])
        self.queue.append(renderer)

        renderer = render.InventoryRenderer(
                self.player.inventory,
                self.tileset,
                self.static_batch,
                None)
        self.queue.append(renderer)

        renderer = render.QuestRenderer(
                self.quest,
                self.player.inventory,
                self.tileset,
                self.static_batch,
                None)
        self.queue.append(renderer)

    def setup_music(self):
        self.music_player = pyglet.media.Player()
        self.music_player.eos_action = self.music_player.EOS_LOOP
        self.music_player.queue(pyglet.resource.media('capewithpatches2.ogg'))
        self.music_player.volume = self.volume
        self.music_player.play()

    def on_draw(self):
        self.think()
        if not self.window:
            return

        if self.music_player.volume < self.volume:
            self.music_player.volume += 0.05

        self.window.clear()
        self.setup_view()
        self.scroll_batch.draw()

        glLoadIdentity()
        self.static_batch.draw()

        glTranslatef(self.tileset.w * 4, 0, 0)
        self.fps.draw()

    def setup_view(self):
        w = self.window.width / 2 - self.tileset.w * 2
        h = self.window.height / 2

        px = self.player.vx * self.tileset.w
        py = self.player.vy * self.tileset.h

        maxx = self.level.w * self.tileset.w - w
        maxy = self.level.h * self.tileset.h - h

        px = min(maxx, max(w, px))
        py = min(maxy, max(h, py))

        glLoadIdentity()
        glTranslatef(
            int(w - px + self.tileset.w * 4),
            int(h - py),
            0,
        )

    def think(self):
        self.safe_call(self.control.think)

        [r.think() for r in self.queue]

        if self.player.won:
            self.app.switch_handler('win', self.music_player)

    def safe_call(self, func, *args, **kwargs):
        try:
            return func(*args, **kwargs)
        except player.InventoryError as err:
            print err.__doc__
