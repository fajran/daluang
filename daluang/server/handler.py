#!/usr/bin/python

import os
from daluang import Config, Reader, Parser, Locator
from django.template.loader import get_template
from django.template import Context
from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseRedirect, Http404

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

data = None
reader = None
main_page = config.read('main_page', 'Wikipedia')

def article(req, lang, article):
	if article == None:
		return HttpResponseRedirect('/%s/article/%s' % (lang, main_page))
		
	while article[-1] == '/':
		article = article[:-1]

	if article.strip() == '':
		return HttpResponseRedirect('/%s/article/%s' % (lang, main_page))

	global data
	if data == None:
		load_data()
	
	reader = load_reader(lang)

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

def search(req, lang, keywords=None):
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
		


def res(req, lang, res):
	html = "res: lang=%s, res=%s" % (lang, res)
	return HttpResponse(html)

def misc(req, lang, item):
	global data
	if data == None:
		load_data()

	html = ""

	if item == None:
		global main_page
		return HttpResponseRedirect('/%s/article/%s' % (lang, main_page))
		
	return HttpResponse(html)

def index(req):
	global data
	if data == None:
		load_data()

	template = get_template('index.html')
	html = template.render(Context({
		'languages': data.values()
	}))

	return HttpResponse(html)

def load_data():
	global data
	global data_dir

	locator = Locator()
	list = locator.scan(data_dir)

	data = {}
	for item in list:
		data[item['code']] = item

def load_reader(lang):
	global data

	if data == None:
		load_data()

	global reader
	if reader == None:
		reader = {}

	try:
		reader[lang]
	except KeyError:
		info = data[lang]
		reader[lang] = Reader(info['datafile'])
	
	return reader[lang]


