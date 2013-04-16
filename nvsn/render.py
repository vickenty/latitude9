from __future__ import division
import os
import pyglet

class Tileset (object):
    w = 16
    h = 16

    def __init__(self):
        self.tiles = {}

    def add(self, name):
        texture = pyglet.resource.image(name + '.png')
        self.tiles[name] = texture

    def __getitem__(self, name):
        return self.tiles[name]

    @classmethod
    def get_default(self):
        tileset = self()
        tileset.add('wall')
        tileset.add('floor')
        tileset.add('player')

        return tileset
 
class LevelRenderer (object):
    def __init__(self, level, tileset, batch, group):
        self.level = level
        self.tileset = tileset
        self.batch = batch
        self.group = group
        self.sprites = {}

    def think(self):
        for cell in self.level.dirty_list:
            if cell.visible:
                self.add_tile(cell)
            else:
                self.del_tile(cell)

        self.level.wipe()

    def add_tile(self, cell):
        tile = self.tileset[cell.name]
        self.sprites[cell.x, cell.y] = sprite = pyglet.sprite.Sprite(tile, batch=self.batch, group=self.group)
        sprite.x = cell.x * self.tileset.w
        sprite.y = cell.y * self.tileset.h

    def del_tile(self, cell):
        try:
            self.sprites[cell.x, cell.y].delete()
            del self.sprites[cell.x, cell.y]
        except KeyError:
            pass

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
