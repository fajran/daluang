#!/usr/bin/python

import os
from xml.dom import minidom

class Locator:
	
	def get_data(self, data_file):
		file = open(data_file)
		tree = minidom.parse(file)

		result = []

		contents = tree.getElementsByTagName("content")
		for content in contents:
			code = self.__get_text(content.getElementsByTagName("code"))
			lang = self.__get_text(content.getElementsByTagName("lang"))
			date = self.__get_text(content.getElementsByTagName("date"))
			data = self.__get_text(content.getElementsByTagName("data"))
			toc = self.__get_text(content.getElementsByTagName("toc"))
			block = self.__get_text(content.getElementsByTagName("block"))

			result.append({
				'code': code,
				'lang': lang,
				'date': date,
				'files': [ data, toc, block ]
			})

		return result

	def __get_text(self, nodes):
		node = nodes[0]
		children = node.childNodes

		text = None
		for child in children:
			if child.nodeType == child.TEXT_NODE:
				text = child.data
				break

		return text

	def scan(self, data_directory):
		list = self.__find_data(data_directory)

		result = []
		for item in list:
			result += self.get_data(os.path.join(data_directory, item))

		return result

	def __find_data(self, data_directory):
		list = os.listdir(data_directory)

		result = []
		for item in list:
			if item.endswith('.xml'):
				result.append(item)

		return result

