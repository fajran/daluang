#!/usr/bin/python

from distutils.core import setup
from os import listdir, path
from glob import glob

#
# Data files
#

data_files = []

# Binaries

data_files.append(('bin', glob('bin/*')))

# Locale files

domain = 'daluang'
languages = ['id']
for lang in listdir('data/locale'):
	if not path.isdir(path.join('data/locale', lang)):
		continue
	if lang[0] == '.':
		continue

	data_files.append((
		'share/daluang/locale/%s/LC_MESSAGES' % lang, 
		[
			'data/locale/%s/LC_MESSAGES/%s.mo' % (lang, domain),
		]
	))

# Icons

for type in listdir('data/browser/icons'):
	data_files.append((
		'share/icons/hicolor/%s/apps' % (type),
		glob('data/browser/icons/%s/apps/*' % (type))
	))

# Browser resources

data_files.append(('share/daluang/browser/res', glob('data/browser/res/*')))

# Server resources

data_files.append(('share/daluang/server/res', glob('data/server/res/*')))
data_files.append(('share/daluang/server/tpl', glob('data/server/tpl/*.tpl')))

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
	('share/daluang/tools', glob('tools/*')),
]

#
# Setup
#

setup(name='daluang',
	version='0.3',
	description='Wikipedia Offline Reader',
	author='Fajran Iman Rusadi',
	author_email='fajran@gmail.com',
	url='http://code.google.com/p/daluang/',
	download_url='http://code.google.com/p/daluang/downloads/list',
	packages=['daluang', 'daluang.browser', 'daluang.server', 'daluang.search'],
	data_files=data_files
)
