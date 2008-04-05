#!/usr/bin/python

from distutils.core import setup

setup(name='daluang',
	version='0.1.5',
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
		('share/icons/hicolor/16x16/apps', ['data/browser/icons/16x16/apps/daluang.png']),
		('share/icons/hicolor/22x22/apps', ['data/browser/icons/22x22/apps/daluang.png']),
		('share/icons/hicolor/24x24/apps', ['data/browser/icons/24x24/apps/daluang.png']),
		('share/icons/hicolor/32x32/apps', ['data/browser/icons/32x32/apps/daluang.png']),
		('share/icons/hicolor/48x48/apps', ['data/browser/icons/48x48/apps/daluang.png']),
		('share/icons/hicolor/64x64/apps', ['data/browser/icons/64x64/apps/daluang.png']),
		('share/icons/hicolor/scalable/apps', ['data/browser/icons/scalable/apps/daluang.svg']),
		('share/daluang/browser/res', [
			'data/browser/res/browser.glade', 
			'data/browser/res/icon.svg',
			'data/browser/res/online.svg',
		]),
		('share/daluang/server/res', [
			'data/server/res/style.css', 
			'data/server/res/index.css',
			'data/server/res/ext.png',
			'data/server/res/jquery.js',
			'data/server/res/article.js'
		]),
		('share/daluang/server/tpl', [
			'data/server/tpl/index.html',
			'data/server/tpl/article.html',
			'data/server/tpl/search_result.html',
			'data/server/tpl/not_found.html'
			'data/server/tpl/unavailable.html'
		])
	]
)
