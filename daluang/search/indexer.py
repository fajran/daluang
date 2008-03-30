
xapian_enabled = True
try:
	import xapian
except ImportError:
	xapian_enabled = False

class Indexer:

	def __init__(self, reader, database, stem_language="none"):
		self.reader = reader
		self.database = database
		self.stem_language = stem_language

	def __init_db(self):
		self.db = xapian.WritableDatabase(self.database, xapian.DB_CREATE_OR_OPEN)
		self.indexer = xapian.TermGenerator()
		self.stemmer = xapian.Stem(self.stem_language)
		self.indexer.set_stemmer(self.stemmer)

	def __add_content(self, title, content, data):
		doc = xapian.Document()
		doc.set_data(data)

		self.indexer.set_document(doc)
		self.indexer.index_text(title)
		self.indexer.index_text(content)

		self.db.add_document(doc)

	def index(self):

		self.__init_db()

		blocks = []
		self.reader.dbc.execute('SELECT DISTINCT block FROM titles')
		for row in self.reader.dbc:
			blocks.append(row[0])

		count = 0
		for block in blocks:
			list = []
			self.reader.dbc.execute('SELECT title, id FROM titles WHERE block=?', (block,))
			for row in self.reader.dbc:
				list.append([row[0], row[1]])

			for item in list:
				print "%d. title:" % count,
				print item[0]

				(title, content) = self.reader.read(item[0])
				self.__add_content(title, content, str(item[1]))

				count += 1
				if count % 1024 == 0:
					print "%d entries processed." % count

		print "Total %d entries processed." % count


