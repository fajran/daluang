#!/usr/bin/python

from distutils.core import setup

setup(name='daluang',
	version='0.1.4',
	description='Wikipedia Dump Reader',
	author='Fajran Iman Rusadi',
	author_email='fajran@gmail.com',
	packages=['daluang', 'daluang.browser', 'daluang.server', 'daluang.search'],
	data_files=[
		('bin', [
			'bin/daluang', 
			'bin/daluang-server', 
			'bin/daluang-browser', 
			'bin/daluang-browser-bin'
		]),
		('share/daluang/example', [
			'example/daluang.conf'
		]),
		('share/applications', [
			'example/daluang.desktop'
		]),
		('share/daluang/data', []),
		('share/daluang/index', []),
		('share/icons/hicolor/icons/16x16/apps', ['data/browser/icons/16x16/apps/daluang.png']),
		('share/icons/hicolor/icons/22x22/apps', ['data/browser/icons/22x22/apps/daluang.png']),
		('share/icons/hicolor/icons/24x24/apps', ['data/browser/icons/24x24/apps/daluang.png']),
		('share/icons/hicolor/icons/32x32/apps', ['data/browser/icons/32x32/apps/daluang.png']),
		('share/icons/hicolor/icons/48x48/apps', ['data/browser/icons/48x48/apps/daluang.png']),
		('share/icons/hicolor/icons/64x64/apps', ['data/browser/icons/64x64/apps/daluang.png']),
		('share/daluang/server/res', [
			'data/server/res/style.css', 
			'data/server/res/index.css',
			'data/server/res/ext.png'
		]),
		('share/daluang/server/tpl', [
			'data/server/tpl/index.html',
			'data/server/tpl/article.html',
			'data/server/tpl/search_result.html',
			'data/server/tpl/not_found.html'
		])
	]
)
