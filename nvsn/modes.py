from __future__ import division
import pyglet
import mode
import math

class WinMode (mode.Mode):
    name = 'win'

    def __init__(self, music_player, text=None):
        super(WinMode, self).__init__()
        self.music_player = music_player
        self.text = text

    def connect(self, app):
        super(WinMode, self).connect(app)

        self.batch = pyglet.graphics.Batch()
        self.label = pyglet.text.Label(
            self.text or "You won!",
            font_name='DejaVu Sans',
            font_size=48,
            x=self.window.width/2,
            y=self.window.height/2,
            anchor_x='center',
            anchor_y='center',
            batch=self.batch)

        self.frame = 0
        self.switch = None

    def on_draw(self):
        self.frame += 1

        if self.switch:
            delta = (self.switch - self.frame) / 60
            self.music_player.volume = delta

        if self.frame == self.switch:
            self.music_player.pause()
            self.app.switch_handler('intro')
            return

        self.window.clear()
        self.batch.draw()

    def on_key_press(self, sym, mods):
        self.switch = self.frame + 60

class IntroMode (mode.Mode):
    name = 'intro'

    def __init__(self):
        super(IntroMode, self).__init__()
        self.scroll_batch = pyglet.graphics.Batch()

        self.label1 = pyglet.text.Label(
                "Nemesis",
                font_name='DejaVu Sans',
                font_size=56,
                x=15,
                y=80)

        self.label2 = pyglet.text.Label(
                "vs",
                font_name='DejaVu Sans Bold',
                font_size=96,
                bold=True,
                x=150,
                y=40,
                color=(255, 0, 0, 255))

        self.label3 = pyglet.text.Label(
                "Nemesis",
                font_name='DejaVu Sans',
                font_size=56,
                x=160,
                y=15)

        self.pak = pyglet.text.Label(
                "Press any key",
                font_name='DejaVu Sans',
                font_size=32,
                x=0,
                y=0,
                anchor_x='center',
                anchor_y='center')

        try:
            music = pyglet.resource.media('blue_curacao.ogg')
        except pyglet.resource.ResourceNotFoundException:
            music = None

        self.music_player = pyglet.media.Player()
        self.music_player.eos_action = self.music_player.EOS_LOOP
        if music is not None:
            self.music_player.queue(music)
        self.music_player.play()
        self.frame = 0
        self.switch = None

    def on_key_press(self, sym, mods):
        self.pak.text = 'Loading'
        self.switch = self.frame + 60

    def on_draw(self):
        self.window.clear()

        if self.switch:
            delta = (self.switch - self.frame) / 60
            self.music_player.volume = delta

        if self.frame == self.switch:
            self.music_player.pause()
            self.app.switch_handler('game')
            return

        self.frame += 1
        self.pak.x = self.window.width // 2
        self.pak.y = self.window.height // 2
        self.pak.color = (255, 255, 255, int(128 + 64 * math.sin(self.frame / 20)))

        self.label1.draw()
        self.label2.draw()
        self.label3.draw()
        self.pak.draw()

class PauseMode (mode.Mode):
    name = 'pause'

    def __init__(self, music_player):
        super(PauseMode, self).__init__()

        self.music_player = music_player

        self.label = pyglet.text.Label(
            'PAUSED',
            font_name='DejaVu Sans',
            font_size=32,
            x=0,
            y=0,
            anchor_x='center',
            anchor_y='center')

        self.frame = 0

    def on_draw(self):
        self.frame += 1
        self.label.x = self.window.width // 2
        self.label.y = self.window.height // 2
        self.label.color = (255, 255, 255, int(128 + 64 * math.sin(self.frame / 20)))

        if self.music_player.volume > 0.1:
            self.music_player.volume -= 0.02

        self.window.clear()
        self.label.draw()

    def on_key_press(self, sym, mods):
        self.app.resume_handler('game')
