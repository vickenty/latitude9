"""Data loaders.

Add functions here to load specific types of resources.

"""

import os
import sys

from pyglet import font
from pyglet import resource

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
resource.path = [os.path.join(DATA_DIR, subdir) for subdir in ['images', 'music', 'sounds']]
resource.reindex()
