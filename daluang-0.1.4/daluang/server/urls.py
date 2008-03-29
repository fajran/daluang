from django.conf.urls.defaults import *
from daluang.server import handler
from daluang import Config

import os

config = Config()
config.init()

res_dir = os.path.join(config.read('base'), 'server/res')

urlpatterns = patterns('',
	(r'^\+res/(?P<path>.*)$', 'django.views.static.serve', {'document_root': res_dir}),
	(r'^([^/]+)/article/(.+)?$', handler.article),
	(r'^([^/]+)/search$', handler.search),
	(r'^([^/]+)/search/(.+)$', handler.search),
	(r'^([^/]+)/(.+)?$', handler.misc),
	(r'^/?$', handler.index),
)
