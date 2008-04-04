
from daluang import Config

import sqlite3
import os
import sha
import time

class Cache:
	
	def __init__(self, cachefile=None, maxsize=500000):
		if cachefile == None:
			config = Config()
			config.init()
			cachefile = config.read("cache", "/tmp/.daluang-%d.cache" % os.getuid())

		self.cachefile = cachefile
		self.maxsize = maxsize

		self.db = sqlite3.connect(self.cachefile)
		self.dbc = self.db.cursor()

		self.__init_db()

	def __init_db(self):
		try:
			self.dbc.execute("CREATE TABLE cache (hash STRING PRIMARY KEY, timestamp INTEGER, content STRING, size INTEGER, pos INTEGER)")
		except sqlite3.OperationalError:
			pass

	def get_hash(self, wiki):
		return sha.new(wiki).hexdigest()

	def get(self, wiki):
		hash = self.get_hash(wiki)
		self.dbc.execute("SELECT hash, timestamp, content FROM cache WHERE hash=?", (hash,))
		row = self.dbc.fetchone()
		
		if row:
			if row[2] >= 0:
				return row[2]

		return None

	def store(self, wiki, html):
		hash = self.get_hash(wiki)
		timestamp = int(time.time())
		cache = html
		size = len(html)
		pos = 0

		values = (hash, timestamp, html, size, pos)

		self.dbc.execute("REPLACE INTO cache (hash, timestamp, content, size, pos) VALUES (?, ?, ?, ?, ?)", values)
		self.dbc.execute("UPDATE cache SET pos = pos + ?", (size,))
		self.dbc.execute("DELETE FROM cache WHERE pos > ?", (self.maxsize,))
		self.db.commit()

	def remove(self, wiki):
		hash = self.get_hash(wiki)
		self.dbc.execute("DELETE FROM cache WHERE hash=?", (hash,))

