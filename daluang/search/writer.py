
from daluang import Reader
from daluang.search import Indexer
import os
import sqlite3

class Writer:

	def __init__(self):
		self.database = None
		self.stem_language = "none"
		self.data = None
		pass

	def set_data(self, data):
		self.data = data

	def set_database(self, database):
		self.database = database

	def set_stem_language(self, stem_language):
		self.stem_language = stem_language

	def index(self):
		reader = Reader(self.data)
		indexer = Indexer(reader, self.database, self.stem_language)
		indexer.index()

		db = sqlite3.connect(self.data)
		dbc = db.cursor()
		dbc.execute("SELECT key, value FROM info")
		for row in dbc:
			if row[0] == 'language':
				language = row[1]
			elif row[0] == 'code':
				code = row[1]
			elif row[0] == 'timestamp':
				timestamp = row[1]

		db.commit()
		db.close()

		db = sqlite3.connect(os.path.join(self.database, 'meta.data'))
		dbc = db.cursor()
		dbc.execute("""CREATE TABLE info (key STRING PRIMARY KEY, value STRING)""")
		dbc.execute("""INSERT INTO info (key, value) VALUES (?, ?)""", ('stemmer', self.stem_language))
		dbc.execute("""INSERT INTO info (key, value) VALUES (?, ?)""", ('language', language))
		dbc.execute("""INSERT INTO info (key, value) VALUES (?, ?)""", ('code', code))
		dbc.execute("""INSERT INTO info (key, value) VALUES (?, ?)""", ('timestamp', timestamp))
		db.commit()
		db.close()

