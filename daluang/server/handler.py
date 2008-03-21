#!/usr/bin/python

import os
from daluang import Config, Reader, Parser, Locator
from django.template.loader import get_template
from django.template import Context
from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseRedirect, Http404
import re

search_enabled = False
try:
	from daluang.search import Finder
	search_enabled = True
except ImportError:
	pass

config = Config()
config.init()

base_dir = config.read('base', '/usr/share/daluang')
data_dir = os.path.join(base_dir, 'data')

server_dir = os.path.join(base_dir, 'server')
resource_dir = os.path.join(server_dir, 'res')
template_dir = os.path.join(server_dir, 'tpl')

handler = None

class Handler:
	
	def __init__(self):
		self.reader = None
		self.base_re = re.compile('http://([^.]+).wikipedia.org/wiki/(.+)')

		self.__load_data()
		self.reader = {}

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

		return res

	def serve_article(self, req, lang, article):
		if not lang in self.languages:
			return HttpResponseRedirect('/')

		article = self.__filter_article(article)
		if article == None:
			return HttpResponseRedirect(self.__get_main_page(lang))

		reader = self.__load_reader(lang)
	
		res = reader.read(article)
		if res == None:
			raise Http404
	
		title, wiki = res
		parser = Parser(wiki)
		parser.set_url_base('/%s/' % lang)
		content = parser.parse()
		
		template = get_template('article.html')
		html = template.render(Context({
			'title': title,
			'content': content,
			'lang': lang
		}))
	
		return HttpResponse(html)
	
	def serve_misc(self, req, lang, item):
	
		html = ""
		if item == None:
			return HttpResponseRedirect(self.__get_main_page(lang))
			
		return HttpResponse(html)
	
	def serve_index(self, req):
	
		template = get_template('index.html')
		html = template.render(Context({
			'languages': self.data.values()
		}))
	
		return HttpResponse(html)
	
	def serve_search(self, req, lang, keywords=None):
		if search_enabled == False:
			template = get_template('search_disabled.html')
			html = template.render(Context({
				'languages': data.values()
			}))
			return HttpResponse(html)
	
		if keywords == None or keywords.strip() == "":
			template = get_template('search_form.html')
			html = template.render(Context({
				'languages': data.values()
			}))
			return HttpResponse(html)
		
		db = ""
		stemmer = ""
	
		finder = Finder(db, stemmer)
		result = finder.find(keywords)
	
		data = []
	
		for item in result:
			rank = item[0]
			percent = item[1]
			id = item[2]
			data = item[3]
		
			p = data.split("\t")
			title = p[1]
			p = p[0].split(" ")
			block_start = int(p[0])
			block_length = int(p[1])
			start = int(p[2])
			length = int(p[3])
	
			data.append([id, percent, rank, title])
		
		template = get_template('search_result.html')
		html = template.render(Context({
			'languages': data.values(),
			'result': data
		}))
		return HttpResponse(html)
			

def init():
	global handler
	if handler == None:
		handler = Handler()

def article(req, lang, article):
	init()
	global handler
	return handler.serve_article(req, lang, article)

def search(req, lang, keywords=None):
	init()
	global handler
	return handler.serve_search(req, lang, keywords)

def misc(req, lang, item):
	init()
	global handler
	return handler.serve_misc(req, lang, item)

def index(req):
	init()
	global handler
	return handler.serve_index(req)


