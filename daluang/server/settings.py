# Django settings for server project.

import daluang
import os

daluang_conf = daluang.Config()
daluang_conf.init()

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1
# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)
ROOT_URLCONF = 'daluang.server.urls'
TEMPLATE_DIRS = (
	os.path.join(daluang_conf.read('base'), 'server/tpl'),
)
