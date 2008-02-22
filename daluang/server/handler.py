#!/usr/bin/python

import os
from daluang import Config, Reader, Parser, Locator
from django.template.loader import get_template
from django.template import Context
from django.conf.urls.defaults import *
from django.http import HttpResponse, HttpResponseRedirect, Http404

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

def search(req, lang):
	html = "search: lang=%s" % (lang)
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
	global data_dir

	if data == None:
		load_data()

	global reader
	if reader == None:
		reader = {}

	try:
		reader[lang]
	except KeyError:
		info = data[lang]
		data_file = os.path.join(data_dir, info['files'][0])
		toc_file = os.path.join(data_dir, info['files'][1])
		block_file = os.path.join(data_dir, info['files'][2])
		reader[lang] = Reader(data_file, toc_file, block_file)
	
	return reader[lang]


