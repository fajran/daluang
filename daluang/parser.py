#!/usr/bin/python

import re
import os

from config import Config

class Parser:

	def __init__(self):
		self.config = Config()
		self.config.init()

		self.ns_media = -2
		self.ns_special = -1
		self.ns_talk = 1
		self.ns_user = 2
		self.ns_user_talk = 3
		self.ns_wikipedia = 4
		self.ns_wikipedia_talk = 5
		self.ns_image = 6
		self.ns_image_talk = 7
		self.ns_mediawiki = 8
		self.ns_mediawiki_talk = 9
		self.ns_template = 10
		self.ns_template_talk = 11
		self.ns_help = 12
		self.ns_help_talk = 13
		self.ns_category = 14
		self.ns_category_talk = 15
		self.ns_portal = 100
		self.ns_portal_talk = 101

		self.__init()
		self.__init_re()

	def parse(self, wiki, code):
		self.__reset()
		html = self.__parse_wiki(wiki, code)
		return html

	def parse_article(self, article, code):
		reader = self.readers.get(code, None)
		if reader:
			wiki = reader.read(article)
			return self.parse(wiki, code)

	def add_reader(self, reader, code):
		self.readers[code] = reader

	def __reset(self):
		self.nowiki = []
		self.references = []

		self.link_external_cnt = 0
		self.link_categories = []
		self.link_translations = []

		self.code = None

		pass


	def __parse_wiki(self, text, code):

		self.code = code

		text = self.__fix_html_entities(text)
		text = self.__remove_comments(text)
		text = self.__parse_nowiki_save(text)
		text = self.__parse_lines(text)
		text = self.__parse_tokens(text)
		text = self.__parse_table(text)
		text = self.__parse_list(text)
		text = self.__parse_preformatted(text)
		text = self.__parse_nowiki_restore(text)
		text = self.__parse_references(text)
		text = self.__make_paragraphs(text)
		text = self.__make_info(text)

		return text

	#
	# Init
	#

	def __init(self):
		# TODO: read from data configuration file since it depends on the language used in content

		self.namespaces = {
			'en': {
				"media":          self.ns_media,
				"special":        self.ns_special,
				"talk":           self.ns_talk,
				"user":           self.ns_user,
				"user_talk":      self.ns_user_talk,
				"wikipedia":      self.ns_wikipedia,
				"wikipedia_talk": self.ns_wikipedia_talk,
				"image":          self.ns_image,
				"image_talk":     self.ns_image_talk,
				"mediawiki":      self.ns_mediawiki,
				"mediawiki_talk": self.ns_mediawiki_talk,
				"template":       self.ns_template,
				"template_talk":  self.ns_template_talk,
				"help":           self.ns_help,
				"help_talk":      self.ns_help_talk,
				"category":       self.ns_category,
				"category_talk":  self.ns_category_talk,
				"portal":         self.ns_portal,
				"portal_talk":    self.ns_portal_talk
			}
		}

		self.namespace_processor = {
			self.ns_media:          self.__ns_media,
			self.ns_special:        self.__ns_special,
			self.ns_talk:           self.__ns_talk,
			self.ns_user:           self.__ns_user,
			self.ns_user_talk:      self.__ns_user_talk,
			self.ns_wikipedia:      self.__ns_wikipedia,
			self.ns_wikipedia_talk: self.__ns_wikipedia_talk,
			self.ns_image:          self.__ns_image,
			self.ns_image_talk:     self.__ns_image_talk,
			self.ns_mediawiki:      self.__ns_mediawiki,
			self.ns_mediawiki_talk: self.__ns_mediawiki_talk,
			self.ns_template:       self.__ns_template,
			self.ns_template_talk:  self.__ns_template_talk,
			self.ns_help:           self.__ns_help,
			self.ns_help_talk:      self.__ns_help_talk,
			self.ns_category:       self.__ns_category,
			self.ns_category_talk:  self.__ns_category_talk,
			self.ns_portal:         self.__ns_portal,
			self.ns_portal_talk:    self.__ns_portal_talk
		}

		# Tokens

		self.tokens = {
			'boldit'  : ["'''''",    "'''''",  self.__parse_boldit   ],
			'pre'     : ['<pre>',    '</pre>', self.__parse_pre      ],
			'bold'    : ["'''",      "'''",    self.__parse_bold     ],
			'italic'  : ["''",       "''",     self.__parse_italic   ],
			'template': ['{{',       '}}',     self.__parse_template ],
			'link'    : ['[[',       ']]',     self.__parse_link     ],
			'elink'   : ['[',        ']',      self.__parse_elink    ]
		}
		self.tokens_order = ['boldit', 'pre', 'bold', 'italic', 'template', 'link', 'elink']
	
		# URL

		self.set_url_base('file://')

		# Language codes

		base = self.config.read('base', '/usr/share/daluang')
		file = os.path.join(base, 'languages.txt')
		f = open(file)
		self.languages = {}
		for line in f:
			(code, language) = line.strip().split("\t")
			self.languages[code] = language

		# Reader
		
		self.readers = {}

	#
	# Namespaces
	#
	def add_namespace(self, code, namespaces):
		self.namespaces[code] = {}
		keys = namespaces.keys()
		for key in keys:
			ns = namespaces[key].lower().replace(" ", "_")
			self.namespaces[code][ns] = key

	#
	# URL
	#

	def set_url_base(self, base):
		if base[-1] != '/':
			base += '/'

		self.url_base = base
		self.set_url_base_image(base + "image/")
		self.set_url_base_article(base + "article/")

	def set_url_base_image(self, base):
		self.url_base_image = base

	def set_url_base_article(self, base):
		self.url_base_article = base


	#
	# Regular expressions
	#

	def __init_re(self):
		
		# Tokens
		self.tokens_open = []
		self.tokens_close = []
		self.tokens_open_map = {}
		self.tokens_close_map = {}

		tokens = []
		escape_re = re.compile('([{}\[\]|])')
		for key in self.tokens_order:
			value = self.tokens[key]

			token_open = value[0]
			token_close = value[1]

			tokens.append(escape_re.sub(r'\\\1', token_close))
			tokens.append(escape_re.sub(r'\\\1', token_open))

			self.tokens_open.append(token_open)
			self.tokens_close.append(token_close)

			self.tokens_open_map[token_open] = key
			self.tokens_close_map[token_close] = key

		patterns = "(" + ")|(".join(tokens) + ")"
		self.tokens_re = re.compile(patterns)

		# Link

		self.link_internal_re = re.compile(r'((([^:]+?):)?([^\|]+))(\|(.*))?')
		self.link_external_re = re.compile(r'([^ ]+)( (.*))?')

		# Misc

		self.heading_re = re.compile('^(=+)\s*([^=]+)\s*(=+)')
		self.break_re = re.compile('^\s*(----+\s*)(.*)$')
		self.comments_re = re.compile(r'<!--.+?-->', re.DOTALL)

		# Language codes

		self.languages_re = re.compile(r'^(%s)$' % "|".join(self.languages.keys()))

	#
	# Comments
	#

	def __remove_comments(self, text):
		return self.comments_re.sub('', text)

	#
	# <nowiki> ... </nowiki>
	#

	def __parse_nowiki_save(self, text):
		self.nowiki = []
		return re.sub('<nowiki>(.+?)</nowiki>', self.__nowiki_save, text)

	def __parse_nowiki_restore(self, text):
		return re.sub('<nowiki></nowiki>', self.__nowiki_restore, text)
	
	def __nowiki_save(self, match):
		self.nowiki.append(match.group(1))
		return '<nowiki></nowiki>'

	def __nowiki_restore(self, match):
		text = self.nowiki[0]
		self.nowiki = self.nowiki[1:]
		return text

	#
	# HTML Entities
	#

	def __fix_html_entities(self, text):
		list = [
			['&lt;', '<'],
			['&gt;', '>'],
			['&quot;', '"'],
			['&apos;', "'"],
			['&amp;', '&']
		]

		for item in list:
			text = text.replace(item[0], item[1])

		return text
	
	#
	# Make paragraphs
	#
	
	def __make_paragraphs(self, text):
		html_re = re.compile('(<[^>]+>)')
		tag_re = re.compile('<(/)?(\w+)(.*)>')

		tag_blocks = ['table', 'tr', 'td', 'th',
			'pre', 'div', 'br',
			'ul', 'ol', 'dl', 'li', 'dd', 'dt', 
			'h2', 'h3', 'h4', 'h5', 'h6', 'h7']

		lines = text.splitlines()
		result = ""

		stack = []
		stack_top = ""
		skip = False
		open = False
		blank = True

		for line in lines:
			
			first = True

			if open and len(stack) == 0 and line.strip() == "":
				open = False
				result += "</p>\n"
				continue

			if line.strip() == "":
				if not blank:
					result += "\n"
				blank = True
				continue

			blank = False

			words = html_re.split(line)
			for word in words:
				if word == "":
					continue

				close = False

				match = tag_re.match(word)
				if match:
					tag = match.group(2)

					if stack_top == tag:
						if match.group(1) != None:
							# Close
							stack = stack[:-1]
							if len(stack) > 0:
								stack_top = stack[-1]
							else:
								stack_stop = ""

							close = True

						else:
							stack.append(tag)
							stack_top = tag

					else:
						stack.append(tag)
						stack_top = tag
				
				if first and not close and not open and (len(stack) == 0 or (not stack_top in tag_blocks)):
					result += '<p>'
					open = True

				result += word
				first = False
	
				if match and match.group(3).endswith('/'):
					stack = stack[:-1]
					if len(stack) > 0:
						stack_top = stack[-1]
					else:
						stack_stop = ""


			if len(stack) > 0:
				result += "\n"
			else:
				result += " "

		if open:	
			result += "</p>"

		return result

	#
	# Parse tokens
	#

	def __parse_tokens(self, text):

		tokens = self.tokens_re.split(text)

		stack = []
		stack_top = None

		result = {}
		pos = 0
		result[0] = ""

		for token in tokens:
			if token == None:
				continue

			if token in self.tokens_close and stack_top == self.tokens_close_map[token]:
				pos -= 1

				try:
					result[pos] += self.__parse_token(stack[-1], result[pos+1])
				except TypeError:
					# When parse_token gives None
					pass

				stack = stack[:-1]
				if len(stack) > 0:
					stack_top = stack[-1]
				else:
					stack_top = None

			elif token in self.tokens_open:
				pos += 1
				result[pos] = ""

				stack.append(self.tokens_open_map[token])
				stack_top = stack[-1]

			else:
				result[pos] += token


		while pos > 0:
			result[pos-1] += result[pos]
			pos -= 1

		return result[0]

	def __parse_token(self, token, text):
		func = self.tokens[token][2]
		return func(text)

	#
	# Link
	#

	def __parse_link(self, text):
		text = text.strip()
		m = self.link_internal_re.match(text)

		if not m:
			return ''

		url = m.group(1)
		label = m.group(6)
		if label == None or label.strip() == "":
			label = url

		if m.group(3) != None:
			tag = m.group(3).lower()

			func = self.__get_ns_processor(tag, self.code)
			if func:
				return func(m)

			else:
				mcode = self.languages_re.match(tag)

				if mcode:
					self.link_translations.append([tag, m.group(4)])

				else:
					return self.__make_ilink(url, label)

		else:
			return self.__make_ilink(url, label)

	def __make_ilink(self, article, label):
		article = (article[0].upper() + article[1:]).replace(' ', '_')
		return '<a href="%s" class="int">%s</a>' % (self.url_base_article + article, label)

	def __parse_elink(self, text):
		text = text.strip()
		m = self.link_external_re.match(text)

		if not m:
			return ''

		url = m.group(1)
		label = m.group(3)
		if label == None or label.strip() == "":
			self.link_external_cnt += 1
			label = "[%d]" % self.link_external_cnt

		return '<a href="%s" class="ext">%s</a>' % (url, label)

	#
	# Namespaces
	#

	def __ns_media(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_special(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_talk(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_user(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_user_talk(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_wikipedia(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_wikipedia_talk(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_image(self, m):
		return '<span class="img"><span>image: %s</span></span>' % (self.url_base_image + m.group(4))

	def __ns_image_talk(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_mediawiki(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_mediawiki_talk(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_template(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_template_talk(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_help(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_help_talk(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_category(self, m):
		self.link_categories.append([m.group(1), m.group(4)])
		return ''

	def __ns_category_talk(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_portal(self, m):
		return self.__make_ilink(m.group(1), m.group(6))

	def __ns_portal_talk(self, m):
		return self.__make_ilink(m.group(1), m.group(6))
		
	def __get_ns_processor(self, tag, code):
		ns = self.namespaces.get(self.code, None)
		if not ns:
			ns = self.namespaces['en']

		type = ns.get(tag, None)
		if type:
			return self.namespace_processor[type]

		# Fallback to english
		ns = self.namespaces['en']

		type = ns.get(tag, None)
		if type:
			return self.namespace_processor[type]

		return None

	#
	# Formatting
	# 

	def __parse_pre(self, text):
		return "<pre>%s</pre>\n" % text

	def __parse_bold(self, text):
		return '<strong>%s</strong>' % text

	def __parse_italic(self, text):
		return '<em>%s</em>' % text

	def __parse_boldit(self, text):
		return self.__parse_bold(self.__parse_italic(text))


	#
	# Template
	#

	def __parse_template(self, text):
		# TODO
		return ''

	#
	# Table
	#

	def __parse_table(self, text):
		lines = text.splitlines()
		result = ""
	
		depth = 0
		table_open = ""
		table_close = {}
		row_open = ""
		row_close = {}
		cell_open = ""
		cell_close = {}

		cell_map = {'||': 'td', '!!': 'th'}

		cell_re = re.compile(r'(\|\|)|(!!)')
		cell_attr_re = re.compile('(([^|]+)\|)?(.+)')

		num = 0

		for line in lines:
			lstrip = line.lstrip()
			lstrip += "  "

			if lstrip[0:2] == "{|":
				depth += 1
				table_open = "<table%s>" % (" " + lstrip[2:].strip())
				table_close[depth] = ""
				row_open = "<tr>"
				row_close[depth] = ""
				cell_close[depth] = ""
				table_caption = ""

			elif depth > 0 and lstrip[0:2] == "|}":
				result += cell_close[depth]
				cell_close[depth] = ""

				result += row_close[depth]
				row_close[depth] = ""

				result += table_close[depth]

				depth -= 1

			elif lstrip[0:2] == '|+':
				table_caption = "<caption>%s</caption>\n" % lstrip[2:].strip()

			elif lstrip[0:2] == '|-':
				result += cell_close[depth]
				cell_close[depth] = ""

				result += row_close[depth]
				row_close[depth] = ""

				row_open = "<tr%s>" % (" " + lstrip[2:].strip())

			elif depth > 0 and lstrip[0:1] in ['|', '!']:
				line = lstrip[0] + lstrip

				cells = cell_re.split(line)
				for cell in cells:
					if cell == None or cell == "":
						continue

					if cell in ['||', '!!']:
						result += cell_close[depth]
						cell_close[depth] = ""

						cell_open = cell_map[cell]

					else:
						if table_open != "":
							if depth > 1:
								result += "\n"
							result += table_open + "\n"
							table_open = ""
							table_close[depth] = "</table>\n"

							result += table_caption
							table_caption = ""

						if row_open != "":
							result += row_open + "\n"
							row_close[depth] = "</%s>\n" % row_open[1:3]
							row_open = ""
						
						if cell_open != "":
							match = cell_attr_re.match(cell)
							if match.group(2) == None:
								result += "<%s>" % cell_open
							else:
								result += "<%s %s>" % (cell_open, match.group(2).strip())
								cell = match.group(3)

							cell_close[depth] = "</%s>\n" % cell_open
							cell_open = ""
							num = 0

						result += "%s" % cell 

			else:
				if num == 0:
					num += 1
					result += "\n"
				result += line + "\n"

		while depth > 0:
			result += cell_close[depth]
			cell_close[depth] = ""

			result += row_close[depth]
			row_close[depth] = ""

			result += table_close[depth]
			table_close[depth] = ""

			depth -= 1
		
		return result

	#
	# List
	#

	def __parse_list(self, text):
		lines = text.splitlines()
		result = ""

		list_re = re.compile('([#*:;]+)([^#*:;].+)')
		list = ""
		list_new = ""

		for line in lines:
			match = list_re.match(line)

			if match:
				if list == "":
					result += "\n"

				list_new = match.group(1)
				result += self.__list_transition(list, list_new)
				list = list_new
				result += match.group(2)

			else:
				transition = self.__list_transition(list, '')
				list = ''

				if (transition != ""):
					result += transition + "\n"

				result += line + "\n"
			
		transition = self.__list_transition(list, '')
		if (transition != ""):
			result += transition + "\n"

		return result

	def __list_transition(self, old, new):

		tag_open = { '#': '<ol>', '*': '<ul>', ':': '<dl>', ';': '<dl>' }
		tag_close = { '#': '</ol>', '*': '</ul>', ':': '</dl>', ';': '</dl>' }
		list_open = { '#': '<li>', '*': '<li>', ':': '<dd>', ';': '<dt>' }
		list_close = { '#': '</li>', '*': '</li>', ':': '</dd>', ';': '</dt>' }

		result = ""

		if old == new:
			if len(old) > 0:
				result += list_close[old[-1]] + "\n" + list_open[old[-1]]
				return result

		open = False

		# closing
		while True:
			if old == new[0:len(old)]:
				break

			result += list_close[old[-1]] + "\n"
			result += tag_close[old[-1]]
			old = old[0:-1]

		# opening
		while True:
			if old == new:
				break

			old += new[len(old)]
			result += tag_open[old[-1]] + "\n"
			result += list_open[old[-1]]
			open = True

		if not open:
			if len(old) > 0:
				result += list_close[old[-1]] + "\n" + list_open[old[-1]]

		return result
		

	# 
	# Preformatted
	#

	def __parse_preformatted(self, text):
		lines = text.splitlines()
		result = ""

		inside = False
		for line in lines:
			if line.startswith(' ') and not inside:
				inside = True
				result += "<pre>\n" + line[1:] + "\n"

			elif inside and not line.startswith(' '):
				inside = False
				result += "</pre>" + "\n" + line + "\n"

			elif inside:
				result += line[1:] + "\n"

			else:
				result += line + "\n"

		return result

	#
	# References
	#

	def __parse_references(self, text):
		ref_re = re.compile('<ref>(.+?)</ref>')
		text = ref_re.sub(self.__collect_references, text)

		data = "<ul>\n"
		for ref in self.references:
			data += "<li>%s</li>\n" % ref
		data += "</ul>\n"

		return text.replace('<references/>', data)

	def __collect_references(self, match):
		self.references.append(match.group(1))
		num = len(self.references)
		return '<sup><a href="#_ref%d">[%d]</a></sup>' % (num, num)

	#
	# Per-line parsing
	#

	def __parse_lines(self, text):
		lines = text.splitlines()
		result = ""

		for line in lines:

			# Heading

			match = self.heading_re.match(line)
			if match:
				result += self.__parse_heading(match) + "\n"
				continue

			# Break
			match = self.break_re.match(line)
			if match:
				result += self.__parse_break(match) + "\n"
				continue

			# else
			result += line + "\n"
		
		return result

	def __parse_heading(self, match):
		num = len(match.group(1))
		return "<h%d>%s</h%d>\n" % (num, match.group(2), num)

	def __parse_break(self, match):
		str = match.group(2).strip()
		if str == "":
			return "<br/>\n"
		else:
			return "<br/>\n\n%s" % str

	#
	# Info box
	#

	def __make_info(self, text):

		data = ""
		data += self.__make_categories()
		data += self.__make_languages()

		if len(data) > 0:
			text += "<div id='info'>\n"
			text += data
			text += "</div>\n"

		return text

	def __make_categories(self):
		result = ""
		
		list = []
		for cat in self.link_categories:
			list.append('<a class="int" href="%s">%s</a>' % (self.url_base_article + cat[0], cat[1]))

		if len(list) > 0:
			result = '<div id="categories"><span class="title">Category:</span> '
			result += " | ".join(list)
			result += '</div>'

		return result

	def __make_languages(self):
		result = ""
		
		self.link_translations.sort(lambda x, y: cmp(self.languages[x[0]], self.languages[y[0]]))

		list = []
		for (code, article) in self.link_translations:
			list.append('<li><a class="int" href="/%s/article/%s/">%s</a>: %s</li>' % (code, article, self.languages[code], article))

		if len(list) > 0:
			result = "<div id='languages'><span class='title'>Other languages:</span> "
			result += "<span class='language-switch pointer' onclick='toggle_language()'>[show]</span>"
			result += "<span style='display:none' class='language-switch pointer' onclick='toggle_language()'>[hide]</span>"
			result += "<ul class='language-switch' style='display:none'>\n"
			result += "\n".join(list)
			result += "\n</ul></div>"

		return result

