#!/usr/bin/python

import bz2
import re
import os
import sqlite3
import sys
import datetime

class Converter:
	
	def __init__(self, input, output):
		self.input = input
		self.output = output

		self.info_code = "en"
		self.info_language = "English"
		self.info_timestamp = datetime.date.today().strftime("%Y%m%d")

	def __flush(self):
		data = bz2.compress(self.buffer)

		self.__add_data(self.block_number, data)

		self.block_number += 1
		self.buffer = ""

	def __add_data(self, block_number, data):
		values = (block_number, sqlite3.Binary(data))
		self.dbc.execute('''INSERT INTO data (block, data) VALUES (?, ?)''', values)

	def __add_toc(self, title, block_number, start, length):
		values = (title.strip(), block_number, start, length)
		self.dbc.execute('''INSERT INTO titles (title, block, start, length) VALUES (?, ?, ?, ?)''', values)

	def __add_namespace(self, key, namespace):
		values = (int(key), namespace)
		self.dbc.execute('''INSERT INTO namespaces (key, namespace) VALUES (?, ?)''', values)

	def __add_info(self, key, value):
		values = (key, value)
		self.dbc.execute('''INSERT INTO info (key, value) VALUES (?, ?)''', values)

	def set_code(self, code):
		self.info_code = code
	
	def set_language(self, language):
		self.info_language = language

	def set_timestamp(self, timestamp):
		self.info_timestamp = timestamp

	def convert(self):
		
		fin = bz2.BZ2File(self.input, "r")
		self.db = sqlite3.connect(self.output)
		self.dbc = self.db.cursor()

		self.dbc.execute('''CREATE TABLE data (block INTEGER, data BLOB)''')
		self.dbc.execute('''CREATE TABLE titles (id INTEGER PRIMARY KEY AUTOINCREMENT, title STRING, block INTEGER, start INTEGER, length INTEGER)''')
		self.dbc.execute('''CREATE TABLE namespaces (key INTEGER, namespace STRING)''')
		self.dbc.execute('''CREATE TABLE info (key STRING PRIMARY KEY, value STRING)''')

		print "Input: %s" % self.input
		print "Output: %s" % self.output
		print "Language: %s" % self.info_language
		print "Code: %s" % self.info_code

		self.__add_info("language", self.info_language)
		self.__add_info("code", self.info_code)
		self.__add_info("timestamp", self.info_timestamp)

		max_block_size = 900 * 1024

		self.block_number = 0
		self.buffer = ""
		
		complete = False
		in_content = False

		entries = 0
		entries_step = 1024

		content_start = False

		metadata = {}
		meta_namespace_re = re.compile('<namespace key="([^"]+)">([^<]+)</namespace>')

		while True:
			line = fin.readline()
	
			if line == "":
				break
			
			line_strip = line.strip()

			if not content_start:
				if line_strip.startswith('<base>'):
					metadata['base'] = line_strip[6:-7]
				elif line_strip.startswith('<namespace key'):
					match = meta_namespace_re.match(line_strip)
					if match:
						self.__add_namespace(match.group(1), match.group(2))
	
			if line_strip.startswith('<title>') and line_strip.endswith('</title>'):
				title = line_strip[7:-8]
				content = ""
				content_start = True
				continue
	
			if line_strip.startswith('<text'):
				if line_strip.endswith('</text>'):
					content = line_strip[27:-7]
					complete = True
				else:
					content = line.lstrip()[27:]
					in_content = True
					continue
	
			if in_content and not complete:
				if line_strip.endswith('</text>'):
					content += line.rstrip()[:-7]
					complete = True
					in_content = False
				else:
					content += line
	
			if complete:
				new_data = "%s\n%s\n" % (title, content)

				if len(new_data) + len(self.buffer) > max_block_size:
					self.__flush()

				start = len(self.buffer)
				self.buffer += new_data
				end = len(self.buffer)

				length = end - start

				self.__add_toc(title, self.block_number, start, length)
					
				complete = False
				in_content = False
	
				entries += 1
				if entries % entries_step == 0:
					print "%d entries processed." % entries

		if len(self.buffer) > 0:
			self.__flush()
			print "%d entries processed." % entries

		for key in metadata:
			self.__add_info(key, metadata[key])

		self.dbc.execute('''CREATE INDEX titles_index ON titles (title)''')

		self.db.commit()
		self.db.close()

		print "done."

