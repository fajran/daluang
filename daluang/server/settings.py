# Django settings for server project.

import daluang
import os
import locale

daluang_conf = daluang.Config()
daluang_conf.init()

DEBUG = True
TEMPLATE_DEBUG = DEBUG

USE_I18N = True

SITE_ID = 1
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
ROOT_URLCONF = 'daluang.server.urls'
TEMPLATE_DIRS = (
	os.path.join(daluang_conf.read('base'), 'server/tpl'),
)
LOCALE_PATHS = (
	os.path.join(daluang_conf.read('base'), 'locale'),
)

LANGUAGE_CODE = locale.getdefaultlocale()[0]
