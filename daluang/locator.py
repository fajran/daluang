#!/usr/bin/python

import os
import sqlite3

class Locator:
	
	def get_data(self, data_file):
		db = sqlite3.connect(data_file)
		dbc = db.cursor()

		dbc.execute('select * from info')

		result = {}
		for row in dbc:
			key = row[0].lower()
			value = row[1]

			if key == 'language':
				result['lang'] = value

			elif key == 'code':
				result['code'] = value

		result['datafile'] = data_file

		db.close()

		return result

	def scan(self, data_directory):
		list = self.__find_data(data_directory)

		result = []
		for item in list:
			result.append(self.get_data(os.path.join(data_directory, item)))

		return result

	def __find_data(self, data_directory):
		list = os.listdir(data_directory)

		result = []
		for item in list:
			if item.endswith('.data'):
				result.append(item)

		return result

