#!/usr/bin/env python

import gtk
import gtk.glade
import gtkmozembed
import sys
import urllib
import webbrowser
import pickle
import os
import re

from daluang import Parser, Reader, Locator, Config

class Browser:
	def __init__(self, base_addr):
		self.base_addr = base_addr.strip(' /')

		self.config = Config()
		self.config.init()

		self.__init_gui_browser()
		self.__init_gui_dialog()
		self.__init_meta()

		self.re_article = re.compile(r'([^/]+)/article/([^/]+)(/|$)')
		self.re_search = re.compile(r'([^/]+)/(article|search|special)/([^/]+)(/|$)')

		self.open_external_browser = None

	def __init_gui_browser(self):
		file = os.path.join(self.config.read('base', '/usr/share/daluang'), "browser/res/browser.glade")
		glade = gtk.glade.XML(file)

		self.window = glade.get_widget("window")

		self.btn_back = glade.get_widget("btn_back")
		self.btn_forward = glade.get_widget("btn_forward")
		self.btn_ok = glade.get_widget("btn_ok")
		self.btn_search = glade.get_widget("btn_search")
		self.btn_home = glade.get_widget("btn_home")
		self.txt_article = glade.get_widget("txt_article")
		self.btn_extra = glade.get_widget("btn_extra")
		self.menu_extra = glade.get_widget("menu_extra")

		self.mi_online = glade.get_widget("mi_online")
		self.mi_all_pages = glade.get_widget("mi_all_pages")

		self.browser = gtkmozembed.MozEmbed()

		browser_container = glade.get_widget("browser_container")
		browser_container.pack_start(self.browser)

		self.browser.show()
		self.browser.load_url(self.base_addr)

		self.window.connect("destroy", self.__on_window_destroy)
		self.btn_back.connect("clicked", self.__on_back_clicked)
		self.btn_forward.connect("clicked", self.__on_forward_clicked)
		self.btn_ok.connect("clicked", self.__on_ok_clicked)
		self.btn_search.connect("clicked", self.__on_search_clicked)
		self.btn_home.connect("clicked", self.__on_home_clicked)
		self.btn_extra.connect("clicked", self.__on_extra_clicked)
		self.txt_article.connect("activate", self.__on_article_changed)
		self.browser.connect("location", self.__on_browser_changed)
		self.browser.connect("open-uri", self.__on_browser_uri_opened)
		self.browser.connect("title", self.__on_browser_title_changed)
		self.browser.connect("net-stop", self.__on_browser_complete)

		self.mi_online.connect("activate", self.__on_online_activated)
		self.mi_all_pages.connect("activate", self.__on_all_pages_activated)

	def __init_gui_dialog(self):
		file = os.path.join(self.config.read('base', '/usr/share/daluang'), "browser/res/external.glade")
		glade = gtk.glade.XML(file)

		self.dialog_external = glade.get_widget('dialog')
		self.dialog_external_url = glade.get_widget('lbl_url')
		self.dialog_external.connect("close", self.__on_dialog_external_closed)

	def __init_meta(self):
		self.meta = {}

		# Get languages

		f = urllib.urlopen("%s/+meta/languages" % self.base_addr)
		p = f.read()
		obj = pickle.loads(p)

		self.meta['languages'] = obj

		self.languages = []
		for lang in obj:
			self.languages.append(lang[0])
		

	# Signals 
	def __on_window_destroy(self, src):
		gtk.main_quit()

	def __on_back_clicked(self, src):
		self.browser.go_back()
		self.__update_button()

	def __on_forward_clicked(self, src):
		self.browser.go_forward()
		self.__update_button()

	def __on_ok_clicked(self, src):
		text = self.txt_article.get_text()
		self.open(text)

	def __on_online_activated(self, src):
		curr = self.browser.get_location()

		skip = len(self.base_addr)
		path = curr[skip:].strip('/ ')
		match = self.re_search.match(path)

		if match:
			lang = match.group(1)
			type = match.group(2)
			article = match.group(3)

			url = None
			if type == "article":
				url = "http://%s.wikipedia.org/wiki/%s" % (lang, article)
			elif type == "search":
				url = "http://%s.wikipedia.org/wiki/Special:Search?search=%s" % (lang, article)

			if url:
				self.__open_external_browser(url)

	def __on_all_pages_activated(self, src):
		self.open(None, type="all_pages")

	def __on_search_clicked(self, src):
		text = self.txt_article.get_text()
		self.open(text, "search")

	def __on_home_clicked(self, src):
		self.browser.load_url(self.base_addr)

	def __on_extra_clicked(self, src):
		self.menu_extra.popup(None, None, self.__get_menu_extra_position, 1, 0)

	def __on_article_changed(self, src):
		text = src.get_text()
		self.open(text)

	def __on_browser_changed(self, src):
		self.__update_button()

	def __on_browser_uri_opened(self, src, uri, data=None):
		if uri.startswith(self.base_addr):
			return False
		else:
			self.__open_external_browser(uri)
			return True

	def __on_browser_complete(self, src, data=None):
		curr = self.browser.get_location()

		skip = len(self.base_addr)
		path = curr[skip:].strip('/ ')

		# Change text in article text field

		match = self.re_article.match(path)
		if match:
			article = match.group(2)
			title = urllib.unquote(article.replace('_', ' '))
			self.txt_article.set_text(title)

		# Toggle open and search button

		match = self.re_search.match(path)
		lang = None
		if match:
			lang = match.group(1)
			status = True
		else:
			status = False

		self.btn_ok.set_sensitive(status)
		self.btn_search.set_sensitive(status)
		self.mi_online.set_sensitive(status)

		if (path == "") or (lang not in self.languages):
			self.mi_all_pages.set_sensitive(False)
		else:
			self.mi_all_pages.set_sensitive(True)


	def __on_browser_title_changed(self, src, data=None):
		title = self.browser.get_title()
		self.window.set_title(title)

	def __update_button(self):
		self.btn_back.set_sensitive(self.browser.can_go_back())
		self.btn_forward.set_sensitive(self.browser.can_go_forward())

	def __on_dialog_external_closed(self, src):
		self.dialog_external.hide()

	# Misc

	def __get_menu_extra_position(self, data):
		(wx, wy) = self.window.window.get_origin()
		(ww, wh) = self.window.get_size()
		(bw, bh) = self.btn_extra.size_request()

		x = wx + ww - bw;
		y = wy + bh;

		return (x, y, True)

	def __open_external_browser(self, uri):
		
		if self.open_external_browser == None:
			self.dialog_external_url.set_text(uri)

			rid = self.dialog_external.run()

			self.dialog_external.hide()

			action = rid > 0

			if rid == 2:
				self.open_external_browser = action

		else:
			action = self.open_external_browser

		if action == True:
			webbrowser.open(uri)

	# Main

	def main(self):
		gtk.main()

	def open(self, article, type="article"):

		skip = len(self.base_addr)
		curr = self.browser.get_location()
		path = curr[skip:].strip('/ ')
		match = self.re_search.match(path)

		lang = None
		if match:
			lang = match.group(1)

		if type in ["all_pages"]:
			url = "%s/%s/special/all" % (self.base_addr, lang)
			self.open_url(url)

		elif type in ["article", "search"]:
			article = article.strip()
			if len(article) == 0:
				return
	
			if match:
				lang = match.group(1)
				url = "%s/%s/%s/%s" % (self.base_addr, lang, type, article)
				self.open_url(url)

	def open_url(self, url):
		self.browser.load_url(url)
		

