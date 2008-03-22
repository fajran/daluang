#!/usr/bin/env python

import gtk
import gtk.glade
import gtkmozembed
import sys
import urllib
import webbrowser
import os
import re

from daluang import Parser, Reader, Locator, Config

class Browser:
	def __init__(self, base_addr):
		self.base_addr = base_addr.strip(' /')

		self.config = Config()
		self.config.init()

		self.gladefile = os.path.join(self.config.read('base', '/usr/share/daluang'), "browser/res/browser.glade")
		self.glade = gtk.glade.XML(self.gladefile)

		self.__init_gui()
		self.__init_signal()

		self.re_article = re.compile(r'([^/]+)/article/([^/]+)(/|$)')

	def __init_gui(self):
		self.window = self.glade.get_widget("window")

		self.btn_back = self.glade.get_widget("btn_back")
		self.btn_forward = self.glade.get_widget("btn_forward")
		self.btn_ok = self.glade.get_widget("btn_ok")
		self.btn_home = self.glade.get_widget("btn_home")
		self.txt_article = self.glade.get_widget("txt_article")

		self.browser = gtkmozembed.MozEmbed()

		browser_container = self.glade.get_widget("browser_container")
		browser_container.pack_start(self.browser)

		self.browser.show()
		self.browser.load_url(self.base_addr)

	def __init_signal(self):
		self.window.connect("destroy", self.__on_window_destroy)
		self.btn_back.connect("clicked", self.__on_back_clicked)
		self.btn_forward.connect("clicked", self.__on_forward_clicked)
		self.btn_ok.connect("clicked", self.__on_ok_clicked)
		self.btn_home.connect("clicked", self.__on_home_clicked)
		self.txt_article.connect("activate", self.__on_article_changed)
		self.browser.connect("location", self.__on_browser_changed)
		self.browser.connect("open-uri", self.__on_browser_uri_opened)
	
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

	def __on_home_clicked(self, src):
		self.browser.load_url(self.base_addr)

	def __on_article_changed(self, src):
		text = src.get_text()
		self.open(text)

	def __on_browser_changed(self, src):
		self.__update_button()

	def __on_browser_uri_opened(self, src, uri, data=None):
		if uri.startswith(self.base_addr):
			return False
		else:
			webbrowser.open(uri)
			return True

	def __update_button(self):
		self.btn_back.set_sensitive(self.browser.can_go_back())
		self.btn_forward.set_sensitive(self.browser.can_go_forward())

	# Main
	def main(self):
		gtk.main()

	def open(self, article):
		article = article.strip()
		if len(article) == 0:
			return

		curr = self.browser.get_location()

		skip = len(self.base_addr)
		path = curr[skip:].strip('/ ')
		match = self.re_article.match(path)

		if match:
			lang = match.group(1)
			url = "%s/%s/article/%s" % (self.base_addr, lang, article)
			self.open_url(url)

	def open_url(self, url):
		self.browser.load_url(url)
		

