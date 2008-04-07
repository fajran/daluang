#!/usr/bin/python

from distutils.core import setup

#
# Data files
#

data_files = []

# Binaries

bins = ['daluang', 'daluang-server', 'daluang-browser', 'daluang-browser-bin']
files = []
for bin in bins:
	files.append('bin/%s' % bin)
data_files.append(('bin', files))

# Locale files

domain = 'daluang'
languages = ['id']
for lang in languages:
	data_files.append((
		'share/daluang/locale/%s/LC_MESSAGES' % lang, 
		[
			'data/locale/%s/LC_MESSAGES/%s.mo' % (lang, domain),
			'data/locale/%s/LC_MESSAGES/django.mo' % (lang)
		]
	))

# Icons

sizes = [16, 22, 24, 32, 48, 64]
for size in sizes:
	data_files.append((
		'share/icons/hicolor/%dx%d/apps' % (size, size),
		['data/browser/icons/%dx%d/apps/daluang.png' % (size, size)]
	))
data_files.append(
	('share/icons/hicolor/scalable/apps', ['data/browser/icons/scalable/apps/daluang.svg'])
)

# Browser resources

res = ['browser.glade', 'icon.svg', 'online.svg']
files = []
for file in res:
	files.append('data/browser/res/%s' % file)
data_files.append(('share/daluang/browser/res', files))

# Server resources

res = ['style.css', 'index.css', 'ext.png', 'jquery.js', 'article.js']
files = []
for file in res:
	files.append('data/server/res/%s' % file)
data_files.append(('share/daluang/server/res', files))

res = ['index.html', 'article.html', 'search_result.html', 'not_found.html', 'unavailable.html']
files = []
for file in res:
	files.append('data/server/tpl/%s' % file)
data_files.append(('share/daluang/server/tpl', files))

# Other files

data_files += [
	('share/daluang', [
		'data/languages.txt'
	]),
	('share/daluang/example', [
		'example/daluang.conf'
	]),
	('share/applications', [
		'example/daluang.desktop'
	]),
	('share/daluang/data', []),
	('share/daluang/index', []),
	('share/daluang/tools', [
		'tools/compile-messages.py',
		'tools/make-messages.py',
	]),
]

#
# Setup
#

setup(name='daluang',
	version='0.2',
	description='Wikipedia Dump Reader',
	author='Fajran Iman Rusadi',
	author_email='fajran@gmail.com',
	url='http://code.google.com/p/daluang/',
	download_url='http://code.google.com/p/daluang/downloads/list',
	packages=['daluang', 'daluang.browser', 'daluang.server', 'daluang.search'],
	data_files=data_files
)
