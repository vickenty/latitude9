"""Data loaders.

Add functions here to load specific types of resources.

"""

import os
import sys

from pyglet import font
from pyglet import media

import config
from common import *
from constants import *

def guess_data_dir():
    for path in DATA_PATH + [os.environ.get('NVSN_DATADIR')]:
        if path and os.access(os.path.join(path, 'nvsn.magic'), os.R_OK):
            print 'Found game data at', path
            return path
    print "Sorry, can't find game data. Please run from the directory"
    print "where run_game.py is located, or set BALLGAME_DATADIR variable."
    sys.exit(1)

DATA_DIR = guess_data_dir()
font.add_directory(os.path.join(DATA_DIR, "fonts"))


def load_file(path, mode="rb"):
    """Open a file.

    :Parameters:
        `path` : str
            The relative path from the data directory to the file.
        `mode` : str
            The mode to use when opening the file (default: "rb").

    """
    file_path = os.path.join(DATA_DIR, path)
    return open(file_path, mode)

def load_song(path):
    """Load a music stream from the music directory.

    :Parameters:
        `path` : str
            The relative path from the music directory to the file.

    """
    song_path = os.path.join(DATA_DIR, "music", path)
    return media.load(song_path)


def load_sound(path):
    """Load a static sound source from the sounds directory.

    :Parameters:
        `path` : str
            The relative path from the sounds directory to the file.

    """
    sound_path = os.path.join(DATA_DIR, "sounds", path)
    return media.load(sound_path, streaming=False)
