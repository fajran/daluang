#!/usr/bin/python

from daluang.converter import Converter
from daluang.reader import Reader
from daluang.parser import Parser
from daluang.locator import Locator
from daluang.config import Config
from daluang.cache import Cache

# Version information

VERSION = '0.3'

# Localization support

import os

config = Config()
config.init()

APPLICATION = "daluang"
LOCALE_DIR = os.path.join(config.read("base", "/usr/share/daluang"), "locale")

import locale
import gettext

modules = [gettext]
try:
	import gtk.glade
	modules.append(gtk.glade)
except ImportError:
	pass

locale.setlocale(locale.LC_ALL, None)
for module in modules:
	module.bindtextdomain(APPLICATION, LOCALE_DIR)
	module.textdomain(APPLICATION)

import __builtin__
__builtin__._ = gettext.gettext

