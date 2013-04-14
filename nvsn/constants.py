"""Constant definitions.

This file is loaded during the program initialisation before the main module is
imported. Consequently, this file must not import any other modules, or those
modules will be initialised before the main module, which means that the DEBUG
value may not have been set correctly.

This module is intended to be imported with 'from ... import *' semantics but
it does not provide an __all__ specification.

"""

#: Enable debug features. Should never be changed manually but is set to True
#: automatically when running `test_game.py`.
DEBUG = False

#: The directory (relative to the top level) wherein all the resources for the
#: game are stored, probably subdivided into types of resources. See `data.py`.
DATA_PATH = [ "data", "../data" ]

#: The name of the game used in locating the saved settings directory. Its best
#: not to have any spaces in this name.
CONFIG_NAME = "nvsn"

#: The caption that appears at the top of the window. Obviously this is only
#: visible in windowed mode.
CAPTION = u"NVSN"

#: The "top-level" tick rate; the maximum number of times per second that the
#: controller will call its tick method.
TICK_RATE = 60.0

#: The "top-level" update rate; the maximum number of times per second that the
#: controller will call its update method.
UPDATE_RATE = 60.0
