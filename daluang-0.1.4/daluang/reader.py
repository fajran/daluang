#!/usr/bin/python

import bz2
import os
import sqlite3

class Reader:

	def __init__(self, data_file):
		self.data_file = data_file

		self.db = sqlite3.connect(self.data_file)
		self.dbc = self.db.cursor()

		self.last_block = None
		self.last_data = None

	def read_info(self, key):
		values = (key,)
		self.dbc.execute('SELECT key, value FROM info WHERE key=?', values)

		row = self.dbc.fetchone()
		if row:
			return row[1]
		else:
			return None

	def read_namespace(self, key):
		values = (key,)
		self.dbc.execute('SELECT key, namespace FROM namespaces WHERE key=?', values)

		row = self.dbc.fetchone()
		if row:
			return row[1]
		else:
			return None

	def read_data(self, block, offset, length):
			
		if block != self.last_block:
			values = (block,)
			self.dbc.execute('SELECT block, data FROM data WHERE block=?', values)
			row = self.dbc.fetchone()

			if row:
				data = row[1]
				data = bz2.decompress(data)

				self.last_data = data
				self.last_block = block

		end = offset + length
		data = self.last_data[offset:end]
		pos = data.index("\n")
		title = data[0:pos]
		content = data[pos+1:]

		return title, content
	
	def read(self, title):
		loc = self.find(title)
		if loc == None:
			return None

		block, offset, length = loc

		return self.read_data(block, offset, length)

	def find(self, title):
	
		# FIXME
		try:
			title = title.strip()
		except:
			title = str(title).strip()

		title = title.replace('_', ' ')
	
		self.dbc.execute('SELECT title, block, start, length FROM titles WHERE title LIKE ?', (title,))

		row = self.dbc.fetchone()
		if row:
			return row[1], row[2], row[3]
		else:
			return None

	def read_title(self, id):
		self.dbc.execute('SELECT title, block, start, length FROM titles WHERE id=?', (id,))
		row = self.dbc.fetchone()

		if row:
			return row[0], row[1], row[2], row[3]
		else:
			return None
			
