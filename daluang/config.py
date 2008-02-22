#!/usr/bin/python

import os
from ConfigParser import SafeConfigParser, NoOptionError, NoSectionError

DEFAULT_CONFIG="/etc/daluang.conf"

class Config:
	def __init__(self, file=DEFAULT_CONFIG):

		list = [
			os.getenv('DALUANG_CONFIG', None),
			file,
			'daluang.conf',
			DEFAULT_CONFIG
		]

		self.files = []
		for item in list:
			if item == None or item in self.files:
				continue
			self.files.append(item)


	def init(self):

		conf = None
		for file in self.files:
			if file != None and os.path.isfile(file):
				conf = file
				break

		if conf == None:
			raise IOError, "Configuration file is missing."

		# parse configuration
		self.cp = SafeConfigParser()
		self.cp.read(file)
	
	def read(self, key, default=None):
		try:
			value = self.cp.get('daluang', key)
			return value
		except:
			return default

