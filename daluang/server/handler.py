#!/usr/bin/python

import os
from daluang import Config, Reader, Parser, Locator, Cache
from daluang.search import Finder
import re

from mako.lookup import TemplateLookup

import urllib


config = Config()
config.init()

base_dir = config.read('base', '/usr/share/daluang')
data_dir = os.path.join(base_dir, 'data')

server_dir = os.path.join(base_dir, 'server')
resource_dir = os.path.join(server_dir, 'res')
template_dir = os.path.join(server_dir, 'tpl')

handler = None

mime_types = {
	'css': 'text/css',
	'html': 'text/html',
	'jpeg': 'image/jpeg',
	'jpg': 'image/jpeg',
	'png': 'image/png'
}

class Handler:
	
	def __init__(self):
		self.reader = None
		self.base_re = re.compile('http://([^.]+).wikipedia.org/wiki/(.+)')

		self.__load_data()
		self.reader = {}

		self.parser = Parser()
		self.cache = Cache()

		# Language index
		file = os.path.join(base_dir, 'languages.txt')
		f = open(file)
		self.language = {}
		for line in f:
			(code, lang) = line.strip().split("\t")
			self.language[code] = lang

		# Template
		global template_dir
		self.template = TemplateLookup(directories=[template_dir])

	def __get_main_page(self, lang):
		reader = self.__load_reader(lang)
		base = reader.read_info('base')
		
		match = self.base_re.match(base)
		if match:
			main_page = match.group(2)
		else:
			main_page = 'Wikipedia'

		return '/%s/article/%s' % (lang, main_page)

	def __load_data(self):
	
		locator = Locator()
		list = locator.scan(data_dir)
	
		self.data = {}
		self.languages = []
		for item in list:
			self.data[item['code']] = item
			self.languages.append(item['code'])

	def __filter_article(self, article):
		if article != None:
			while article[-1] == '/':
				article = article[:-1]

			if article.strip() != '':
				return article.strip()

		return None

	def __load_reader(self, lang):
	
		res = self.reader.get(lang, None)
		if res == None:
			self.reader[lang] = Reader(self.data[lang]['datafile'])
			res = self.reader[lang]

		self.parser.add_namespace(lang, self.reader[lang].get_namespaces())
		self.parser.add_reader(self.reader[lang], lang)

		return res

	def serve_article(self, req, lang, article):
		#print _
		#print req.LANGUAGE_CODE

		if not lang in self.languages:
			return self._redirect(req, '/')

		article = self.__filter_article(article)
		if article == None:
			return self._redirect(req, self.__get_main_page(lang))

		reader = self.__load_reader(lang)
	
		res = reader.read(article)
		if res == None:
			return self.serve_not_found(req, lang, article)
	
		title, wiki = res
		self.parser.set_url_base('/%s/' % lang)
		content = self.cache.get(wiki)
		if content == None:
			content = self.parser.parse(wiki, lang)
			self.cache.store(wiki, content)
		
		template = self.template.get_template('article.tpl')
		html = template.render(
			title=title,
			content=content,
			lang=lang
		)
	
		return self._response(req, html)

	def serve_unavailable(self, req, lang, article):
		article = self.__filter_article(article)
		article = article.replace('_', ' ')

		template = self.template.get_template('unavailable.html')
		html = template.render(
			article=article,
			lang=lang,
			language=self.language[lang]
		)

		self._response(req, html)

	def serve_not_found(self, req, lang, article):

		article = self.__filter_article(article)
		article = article.replace('_', ' ')

		template = self.template.get_template('not_found.tpl')
		html = template.render(
			article=article,
			lang=lang
		)
	
		return self._response(req, html, code=404)

	def _redirect(self, req, target):
		print "redirect:", target
		req.send_response(307)
		req.send_header('location', target)
		req.end_headers()

		return True

	def _response(self, req, data, mime="text/html", code=200):
		req.send_response(code)
		req.send_header('content-type', mime)
		req.end_headers()
		req.wfile.write(data)

		return True
	
	def serve_misc(self, req, lang, item):
		if not lang in self.languages:
			return self._redirect(req, '/')
	
		html = ""
		if item == None:
			return self._redirect(req, self.__get_main_page(lang))
			
		return self._response(req, html, 'text/html')
	
	def serve_index(self, req):
	
		template = self.template.get_template("index.tpl")
		html = template.render(
			languages=self.data.values()
		)
		self._response(req, html)

	def serve_static(self, req, path):
		global resource_dir, mime_types

		p = path.split('.')
		if len(p) > 0:
			ext = p[-1]
			mime = mime_types.get(ext, 'text/plain')
		else:
			mime = 'text/plain'

		# TODO: check file existance
		f = open(os.path.join(resource_dir, path))

		req.send_response(200)
		req.send_header('Content-type', mime)
		req.end_headers()

		req.wfile.write(f.read())
	
	def serve_search(self, req, lang, keywords=None):
		if not lang in self.languages:
			return self._redirect(req, '/')

		keywords = self.__filter_article(keywords)
		keywords = keywords.replace('_', ' ')

		if keywords == None or keywords.strip() == "":
			# FIXME: search_form.tpl is not available
			template = self.template.get_template('search_form.tpl')
			html = template.render(
				languages=data.values()
			)
			return self._response(req, html)
		
		reader = self.__load_reader(lang)
			
		db = ""
		stemmer = ""
	
		finder = Finder(reader)
		result = finder.find(keywords)
	
		data = []
	
		for item in result:
			data_id = int(item[0])
			rank = item[1]
			percent = item[2]
			did = item[3]
		
			reader = self.__load_reader(lang)
			res = reader.read_title(data_id)

			if not res:
				# FIXME
				continue

			(title, block, start, length) = res

			data.append([data_id, title, percent, rank])
		
		template = self.template.get_template('search_result.tpl')
		html = template.render(
			keywords=keywords,
			lang=lang,
			result=data
		)
		return self._response(req, html)
			

from BaseHTTPServer import BaseHTTPRequestHandler

class DaluangHandler(BaseHTTPRequestHandler):

	handler = Handler()
	initialized = False

	def __init(self):

		urlpatterns = (
			(r'^/\+res/(?P<path>.*)$', self.handler.serve_static),
			(r'^/([^/]+)/article/(.+)?$', self.handler.serve_article),
			(r'^/([^/]+)/search$', self.handler.serve_search),
			(r'^/([^/]+)/search/(.+)$', self.handler.serve_search),
			(r'^/([^/]+)/(.+)?$', self.handler.serve_misc),
			(r'^/?$', self.handler.serve_index),
		)

		self.urls = []
		for p in urlpatterns:
			pattern = p[0]
			h = p[1]
			c = re.compile(pattern)

			self.urls.append((c, h))


	def do_GET(self):
		
		if not self.initialized:
			self.__init()

		path = urllib.unquote(self.path)

		for url in self.urls:
			r = url[0]
			f = url[1]
			match = r.match(path)
			if match:
				param = match.groups()
				f(self, *param)
				return True


		self.send_response(404)

		self.send_header('Content-type', 'text/html')
		self.end_headers()

		self.wfile.write("<strong>File not found</strong>")


		
	



