from __future__ import division
import os
import pyglet
from pyglet.gl import *

class Tileset (object):
    w = 32
    h = 32

    def __init__(self):
        self.tiles = {}

    def add(self, name, fname=None, rows=None, cols=None):
        fname = fname or (name + '.png')
        texture = pyglet.resource.image(fname)
        glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        if rows and cols:
            grid = pyglet.image.ImageGrid(texture, rows, cols)
            texture = pyglet.image.Animation([
                pyglet.image.AnimationFrame(grid[i], 0.1)
                for i in range(rows * cols)])
        self.tiles[name] = texture

    def __getitem__(self, name):
        return self.tiles[name]

    @classmethod
    def get_default(self):
        tileset = self()
        tileset.add('wall')
        tileset.add('floor')
        tileset.add('shovel')
        tileset.add('pit')
        tileset.add('trap')
        tileset.add('exit')
        tileset.add('mine')
        tileset.add('minekit')
        tileset.add('gem1', 'crystal-qubodup-ccby3/crystal-qubodup-ccby3-32-blue.png', 1, 8)
        tileset.add('gem2', 'crystal-qubodup-ccby3/crystal-qubodup-ccby3-32-green.png', 1, 8)
        tileset.add('gem3', 'crystal-qubodup-ccby3/crystal-qubodup-ccby3-32-grey.png', 1, 8)
        tileset.add('gem4', 'crystal-qubodup-ccby3/crystal-qubodup-ccby3-32-orange.png', 1, 8)
        tileset.add('gem5', 'crystal-qubodup-ccby3/crystal-qubodup-ccby3-32-pink.png', 1, 8)
        tileset.add('gem6', 'crystal-qubodup-ccby3/crystal-qubodup-ccby3-32-yellow.png', 1, 8)

        return tileset

class LevelRenderer (object):
    visibility_types = {
        0: 0,
        1: 127,
        2: 255
    }

    def __init__(self, owner, level, tileset, batch, tiles_group, items_group):
        self.owner = owner
        self.visibility = owner.visibility
        self.level = level
        self.tileset = tileset
        self.batch = batch
        self.tiles_group = tiles_group
        self.items_group = items_group
        self.sprites = {}
        self.item_sprites = {}

        self.build_sprites()

    def build_sprites(self):
        for x in range(0, self.level.w):
            for y in range(0, self.level.h):
                cell = self.level[x, y]
                self.add_tile(self.sprites, cell.name, (x, y))

    def think(self):
        for cell in self.visibility.dirty_list:
            pos = cell.x, cell.y
            vis = self.visibility[cell]
            self.sprites[pos].opacity = self.visibility_types[vis]

            if vis == cell.LIT and (cell.item or cell.trap):
                if cell.item and pos not in self.item_sprites:
                    self.add_tile(self.item_sprites, cell.item.name, pos, self.items_group)

                if cell.trap and cell.trap.owner == self.owner and pos not in self.item_sprites:
                    self.add_tile(self.item_sprites, cell.trap.name, pos, self.items_group)

            else:
                if pos in self.item_sprites:
                    self.item_sprites[pos].delete()
                    del self.item_sprites[pos]

        self.visibility.wipe()

    def add_tile(self, container, name, pos, group=None):
        if not group:
            group = self.tiles_group
        tile = self.tileset[name]
        container[pos] = sprite = pyglet.sprite.Sprite(tile, batch=self.batch, group=self.tiles_group)
        sprite.x = pos[0] * self.tileset.w
        sprite.y = pos[1] * self.tileset.h

class PlayerRenderer (object):
    def __init__(self, player, tileset, batch, group):
        self.player = player
        self.tileset = tileset
        self.batch = batch
        self.group = group
        self.last_move = (0, -1)
        self.anims = {}
        self.still = {}

        self.setup_sprites()

    anim_defs = [
        ((0, -1), [9, 10, 11]),
        ((-1, 0), [6, 7, 8]),
        ((1, 0), [3, 4, 5]),
        ((0, 1), [0, 1, 2]),
    ]

    def setup_sprites(self):
        grid = pyglet.image.ImageGrid(pyglet.resource.image('player1.png'), 4, 3)
        for move, animdef in self.anim_defs:
            anim = pyglet.image.Animation([pyglet.image.AnimationFrame(grid[frame], 0.05) for frame in animdef])
            self.anims[move] = anim
            self.still[move] = grid[animdef[1]]

        self.trapped = pyglet.resource.image('trapped.png')

        self.sprite = pyglet.sprite.Sprite(self.still[0, -1], batch=self.batch, group=self.group)

    def think(self):
        if not self.player.alive:
            self.sprite.opacity = 0
            return
        else:
            self.sprite.opacity = 255

        if self.player.dx or self.player.dy:
            self.last_move = self.player.dx, self.player.dy
            newanim = self.anims[self.last_move]
        else:
            newanim = self.still[self.last_move]

        if self.player.state == self.player.TRAPPED:
            newanim = self.trapped

        if newanim != self.sprite.image:
            self.sprite.image = newanim

        self.sprite.x = self.player.vx * self.tileset.w
        self.sprite.y = self.player.vy * self.tileset.h

class QuestRenderer (object):
    def __init__(self, quest, inventory, tileset, batch, group):
        self.quest = quest
        self.inventory = inventory
        self.tileset = tileset
        self.batch = batch
        self.group = group

        self.sprites = []

        self.build()

    def build(self):
        for slot, name in enumerate(self.quest.goals):
            tile = self.tileset[name]
            sprite = pyglet.sprite.Sprite(tile, batch=self.batch, group=self.group)
            sprite.x = self.tileset.w
            sprite.y = self.tileset.h * (1.5 * slot + 10)
            self.sprites.append(sprite)

    def think(self):
        has = self.inventory.item_types()
        for slot, name in enumerate(self.quest.goals):
            self.sprites[slot].opacity = 127 + 127 * (name in has)

class InventoryRenderer (object):
    def __init__(self, inventory, tileset, batch, group):
        self.inventory = inventory
        self.tileset = tileset
        self.batch = batch
        self.group = group
        self.sprites = {}

    def think(self):
        sprites = self.sprites
        for slot, item in enumerate(self.inventory.items):

            if item and slot not in self.sprites:
                offset = self.tileset.h * (1.5 * slot + 1)
                sprites[slot] = self.add_sprite(item.name, offset)
            if not item and slot in self.sprites:
                sprites[slot].delete()
                del sprites[slot]

    def add_sprite(self, name, offset):
        tile = self.tileset[name]
        sprite = pyglet.sprite.Sprite(tile, batch=self.batch, group=self.group)
        sprite.x = self.tileset.w
        sprite.y = offset
        return sprite

if __name__ == '__main__':
    import level, data

    tileset = Tileset.get_default()

    level = level.Dummy(15, 15)
    level.generate()
    level.update_visibility(7, 7, 7)

    batch = pyglet.graphics.Batch()
    renderer = LevelRenderer(level, tileset, batch, None)
    renderer.think()

    win = pyglet.window.Window()

    @win.event
    def on_draw():
        batch.draw()

    pyglet.app.run()
