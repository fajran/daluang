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
		('share/daluang/data', []),
		('share/daluang/index', []),
		('share/daluang/browser/res', [
			'data/browser/res/browser.glade'
		]),
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
