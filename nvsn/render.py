from __future__ import division
import os
import pyglet
from pyglet.gl import *

class Tileset (object):
    w = 16
    h = 16

    def __init__(self):
        self.tiles = {}

    def add(self, name):
        texture = pyglet.resource.image(name + '.png')
        glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        self.tiles[name] = texture

    def __getitem__(self, name):
        return self.tiles[name]

    @classmethod
    def get_default(self):
        tileset = self()
        tileset.add('wall')
        tileset.add('floor')
        tileset.add('player')
        tileset.add('shovel')
        tileset.add('pit')
        tileset.add('trap')
        tileset.add('gem1')
        tileset.add('gem2')
        tileset.add('gem3')
        tileset.add('flower1')
        tileset.add('flower2')
        tileset.add('flower3')
        tileset.add('exit')
        tileset.add('mine')
        tileset.add('minekit')

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

        self.setup_sprites()

    def setup_sprites(self):
        tile = self.tileset['player']
        self.sprite = pyglet.sprite.Sprite(tile, batch=self.batch, group=self.group)

    def think(self):
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
            sprite.y = self.tileset.h * (3 * slot + 20)
            sprite.scale = 2
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
                offset = self.tileset.h * (3 * slot + 1)
                sprites[slot] = self.add_sprite(item.name, offset)
            if not item and slot in self.sprites:
                sprites[slot].delete()
                del sprites[slot]

    def add_sprite(self, name, offset):
        tile = self.tileset[name]
        sprite = pyglet.sprite.Sprite(tile, batch=self.batch, group=self.group)
        sprite.x = self.tileset.w
        sprite.y = offset
        sprite.scale = 2
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
