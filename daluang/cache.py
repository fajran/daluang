
from daluang import Config

import sqlite3
import os
import sha
import time

class Cache:
	
	def __init__(self, cachefile=None, maxsize=500000):
		config = Config()
		config.init()

		# State
		self.enabled = True
		enabled = config.read("caching", "True").lower()
		if not enabled in ["1", "true", "enable", "enabled", "on"]:
			self.enabled = False

		if not self.enabled:
			return

		# Cache file
		if cachefile == None:
			cachefile = config.read("cache", '/tmp/.daluang-%u.cache')

		self.cachefile = cachefile.replace('%u', str(os.getuid()))

		# Size
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
		if not self.enabled:
			return None

		hash = self.get_hash(wiki)
		self.dbc.execute("SELECT hash, timestamp, content FROM cache WHERE hash=?", (hash,))
		row = self.dbc.fetchone()
		
		if row:
			if row[2] >= 0:
				return row[2]

		return None

	def store(self, wiki, html):
		if not self.enabled:
			return

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
		if not self.enabled:
			return

		hash = self.get_hash(wiki)
		self.dbc.execute("DELETE FROM cache WHERE hash=?", (hash,))

