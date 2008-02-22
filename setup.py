#!/usr/bin/python

from distutils.core import setup

setup(name='daluang',
	version='0.1.1',
	description='Wikipedia Dump Reader',
	author='Fajran Iman Rusadi',
	author_email='fajran@gmail.com',
	packages=['daluang', 'daluang.browser', 'daluang.server'],
	data_files=[
		('bin', ['bin/daluang', 'bin/daluang-server', 'bin/daluang-browser']),
		('share/daluang/example', ['example/daluang.conf']),
		('share/daluang/data', []),
		('share/daluang/browser/res', ['data/browser/res/browser.glade']),
		('share/daluang/server/res', ['data/server/res/style.css']),
		('share/daluang/server/tpl', ['data/server/tpl/index.html','data/server/tpl/article.html'])
	]
)
