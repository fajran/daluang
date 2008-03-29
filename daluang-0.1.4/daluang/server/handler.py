#!/usr/bin/python

import os
from daluang import Config, Reader, Parser, Locator
from daluang.search import Finder
from django.template.loader import get_template
from django.template import Context
from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect, Http404
import re

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
			return self.serve_not_found(req, lang, article)
	
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

	def serve_not_found(self, req, lang, article):

		article = self.__filter_article(article)
		article = article.replace('_', ' ')

		template = get_template('not_found.html')
		html = template.render(Context({
			'article': article,
			'lang': lang
		}))
	
		return HttpResponseNotFound(html)
	
	def serve_misc(self, req, lang, item):
		if not lang in self.languages:
			return HttpResponseRedirect('/')
	
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
		if not lang in self.languages:
			return HttpResponseRedirect('/')

		keywords = self.__filter_article(keywords)
		keywords = keywords.replace('_', ' ')

		if keywords == None or keywords.strip() == "":
			template = get_template('search_form.html')
			html = template.render(Context({
				'languages': data.values()
			}))
			return HttpResponse(html)
		
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
		
		template = get_template('search_result.html')
		html = template.render(Context({
			'keywords': keywords,
			'lang': lang,
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


