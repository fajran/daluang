
from daluang import Config
import os
import sqlite3

xapian_enabled = True
try:
	import xapian
except ImportError:
	xapian_enabled = False


class Finder:

	def __init__(self, reader):
		self.reader = reader
		self.code = reader.read_info("code")

		self.use_xapian = False
		if xapian_enabled:
			self.use_xapian = self.__xapian_init()

	def find(self, keywords, total=10):
		
		if self.use_xapian:
			result = self.__xapian_find(keywords, total)
		else:
			result = self.__simple_find(keywords)

		return result

	def __simple_find(self, keywords):
		result = []

		self.reader.dbc.execute('SELECT id FROM titles WHERE title LIKE ?', ('%%%s%%' % keywords,))
		for row in self.reader.dbc:
			result.append([row[0], None, None, None])

		return result

	def __xapian_init(self):

		config = Config()
		config.init()

		base_dir = config.read('base')
		database = os.path.join(base_dir, 'index', self.code)
		meta = os.path.join(database, 'meta.data')

		if not os.path.exists(meta):
			return False

		db = sqlite3.connect(meta)
		dbc = db.cursor()
		dbc.execute('SELECT value FROM info WHERE key=?', ('stemmer',))
		row = dbc.fetchone()

		stem_language = "none"
		if row:
			stem_language = row[0]


		self.db = xapian.Database(database)
		self.enquire = xapian.Enquire(self.db)
		self.stemmer = xapian.Stem(stem_language)

		self.qp = xapian.QueryParser()
		self.qp.set_stemmer(self.stemmer)
		self.qp.set_database(self.db)
		self.qp.set_stemming_strategy(xapian.QueryParser.STEM_SOME)

		return True

	def __xapian_find(self, keywords, total=10):
		query = self.qp.parse_query(keywords)
		self.enquire.set_query(query)

		matches = self.enquire.get_mset(0, total)

		result = []
		for m in matches:
			result.append([int(m[xapian.MSET_DOCUMENT].get_data()), m[xapian.MSET_RANK], m[xapian.MSET_PERCENT], m[xapian.MSET_DID]])

		return result

