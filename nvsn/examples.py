"""Example implementation.

Simple two mode structure, press the space bar to toggle and escape to quit.
Displays an additional label if DEBUG is enabled, try running run_game.py and
test_game.py.

"""

from __future__ import division

from pyglet import text
from pyglet.event import EVENT_HANDLED
from pyglet.event import EVENT_UNHANDLED
from pyglet.window import key

import mode

import config
from common import *
from constants import *


menu_label = text.Label("MENU", font_size=20)
game_label = text.Label("GAME", font_size=20)
debug_label = text.Label("DEBUG", font_size=20, y=24)


## Menu
#######

class MenuMode(mode.Mode):
    name = "menu"

    def __init__(self):
        super(MenuMode, self).__init__()

    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.control.switch_handler("game")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

    def on_draw(self):
        self.window.clear()
        menu_label.draw()
        if DEBUG:
            debug_label.draw()


## Game
#######

class GameMode(mode.Mode):
    name = "game"

    def on_key_press(self, sym, mods):
        if sym == key.SPACE:
            self.control.switch_handler("menu")
        else:
            return EVENT_UNHANDLED
        return EVENT_HANDLED

    def on_draw(self):
        self.window.clear()
        game_label.draw()
        if DEBUG:
            debug_label.draw()
