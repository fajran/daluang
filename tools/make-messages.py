#!/usr/bin/env python

# Need to ensure that the i18n framework is enabled
from django.conf import settings
settings.configure(USE_I18N = True)

from django.utils.translation import templatize
import re
import os
import sys
import getopt

pythonize_re = re.compile(r'\n\s*//')

binfiles = ["daluang", "daluang-server", "daluang-browser", "daluang-browser-bin"]

def make_messages():
	localedir = 'data/locale'

	(opts, args) = getopt.getopt(sys.argv[1:], 'l:va')

	lang = None
	verbose = False
	domain = "daluang"
	all = False

	for o, v in opts:
		if o == '-l':
			lang = v
		elif o == '-v':
			verbose = True
		elif o == '-a':
			all = True

	if (lang is None and not all) or domain is None:
		print "usage: make-messages.py -l <language>"
		print "   or: make-messages.py -a"
		sys.exit(1)

	languages = []

	if lang is not None:
		languages.append(lang)
	elif all:
		languages = [el for el in os.listdir(localedir) if not el.startswith('.')]

	for lang in languages:

		print "processing language", lang
		basedir = os.path.join(localedir, lang, 'LC_MESSAGES')
		if not os.path.isdir(basedir):
			os.makedirs(basedir)

		pofile = os.path.join(basedir, '%s.po' % domain)
		potfile = os.path.join(basedir, '%s.pot' % domain)

		if os.path.exists(potfile):
			os.unlink(potfile)

		for (dirpath, dirnames, filenames) in os.walk("."):
			for file in filenames:
				if file.endswith('.py') or file.endswith('.html') or (dirpath.startswith('./bin') and (file in binfiles)):
					thefile = file
					if file.endswith('.html'):
						src = open(os.path.join(dirpath, file), "rb").read()
						open(os.path.join(dirpath, '%s.py' % file), "wb").write(templatize(src))
						thefile = '%s.py' % file
					if verbose: sys.stdout.write('processing file %s in %s\n' % (file, dirpath))
					cmd = 'xgettext %s -d %s -L Python --keyword=gettext_noop --keyword=gettext_lazy --keyword=ngettext_lazy --from-code UTF-8 -o - "%s"' % (
						os.path.exists(potfile) and '--omit-header' or '', domain, os.path.join(dirpath, thefile))
					(stdin, stdout, stderr) = os.popen3(cmd, 'b')
					msgs = stdout.read()
					errors = stderr.read()
					if errors:
						print "errors happened while running xgettext on %s" % file
						print errors
						sys.exit(8)
					if thefile != file:
						old = '#: '+os.path.join(dirpath, thefile)[2:]
						new = '#: '+os.path.join(dirpath, file)[2:]
						msgs = msgs.replace(old, new)
					if msgs:
						open(potfile, 'ab').write(msgs)
					if thefile != file:
						os.unlink(os.path.join(dirpath, thefile))

		if os.path.exists(potfile):
			(stdin, stdout, stderr) = os.popen3('msguniq "%s"' % potfile, 'b')
			msgs = stdout.read()
			errors = stderr.read()
			if errors:
				print "errors happened while running msguniq"
				print errors
				sys.exit(8)
			open(potfile, 'w').write(msgs)
			if os.path.exists(pofile):
				(stdin, stdout, stderr) = os.popen3('msgmerge -q "%s" "%s"' % (pofile, potfile), 'b')
				msgs = stdout.read()
				errors = stderr.read()
				if errors:
					print "errors happened while running msgmerge"
					print errors
					sys.exit(8)
			open(pofile, 'wb').write(msgs)
			os.unlink(potfile)

if __name__ == "__main__":
	make_messages()
