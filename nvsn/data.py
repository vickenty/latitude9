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

resource.path = [os.path.join("data", subdir) for subdir in ['fonts', 'images', 'music', 'sounds']]
resource.reindex()
