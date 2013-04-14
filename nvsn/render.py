import os
import pyglet

class Tileset (object):
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

    def update(self):
        for cell in self.level.dirty_list:
            if cell.visible:
                self.add_tile(cell)
            else:
                self.del_tile(cell)

        self.level.wipe()

    def add_tile(self, cell):
        tile = self.tileset[cell.name]
        self.sprites[cell.x, cell.y] = sprite = pyglet.sprite.Sprite(tile, batch=self.batch, group=self.group)
        sprite.x = cell.x * 16
        sprite.y = cell.y * 16

    def del_tile(self, cell):
        del self.sprites[cell.x, cell.y]

if __name__ == '__main__':
    import level, data

    tileset = Tileset.get_default()

    level = level.Dummy(15, 15)
    level.generate()

    batch = pyglet.graphics.Batch()
    renderer = LevelRenderer(level, tileset, batch, None)
    renderer.update()

    win = pyglet.window.Window()

    @win.event
    def on_draw():
        batch.draw()

    pyglet.app.run()
