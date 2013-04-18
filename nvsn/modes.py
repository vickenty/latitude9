import pyglet
import mode

class WinMode (mode.Mode):
    name = 'win'

    def __init__(self):
        super(WinMode, self).__init__()

    def connect(self, app):
        super(WinMode, self).connect(app)

        self.batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label("You won!", 
            font_size=48,
            x=self.window.width/2,
            y=self.window.height/2,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch)

    def on_draw(self):
        self.window.clear()
        self.batch.draw()
