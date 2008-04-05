#!/usr/bin/python

from daluang.converter import Converter
from daluang.reader import Reader
from daluang.parser import Parser
from daluang.locator import Locator
from daluang.config import Config
from daluang.cache import Cache

# Localization support

import os

config = Config()
config.init()

APPLICATION = "daluang"
LOCALE_DIR = os.path.join(config.read("base", "/usr/share/daluang"), "locale")

import locale
import gettext

locale.setlocale(locale.LC_ALL, None)
gettext.bindtextdomain(APPLICATION, LOCALE_DIR)
gettext.textdomain(APPLICATION)

import __builtin__
__builtin__._ = gettext.gettext

