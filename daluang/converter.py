#!/usr/bin/python

import bz2
import re
import os

class Converter:
	
	def __init__(self, input, output_data, output_toc, output_block):
		self.input = input
		self.output_data = output_data
		self.output_toc = output_toc
		self.output_toc_tmp = output_toc + ".tmp"
		self.output_block = output_block

	def __flush(self):
		data = bz2.compress(self.buffer)
		self.buffer = ""

		block_start = self.fout.tell()
		self.fout.write(data)
		block_end = self.fout.tell()

		length = block_end - block_start
		self.fblock.write("%d %d %d\n" % (self.block_number, block_start, length))

		self.block_number += 1

	def convert(self):
		
		fin = bz2.BZ2File(self.input, "r")
		ftoctmp = open(self.output_toc_tmp, "w")
		self.fout = open(self.output_data, "w")
		self.fblock = open(self.output_block, "w")

		print "Input: %s" % self.input
		print "Output data: %s" % self.output_data
		print "Output table of contents: %s" % self.output_toc
		print "Output block info: %s" % self.output_block

		max_block_size = 900 * 1024

		self.block_number = 0
		self.buffer = ""
		
		complete = False
		in_content = False

		entries = 0
		entries_step = 1024

		while True:
			line = fin.readline()
	
			if line == "":
				break
			
			line_strip = line.strip()
	
			if line_strip.startswith('<title>') and line_strip.endswith('</title>'):
				title = line_strip[7:-8]
				content = ""
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

				ftoctmp.write("%s\t%d\t%d\t%d\n" % (title.lower(), self.block_number, start, length))
					
				complete = False
				in_content = False
	
				entries += 1
				if entries % entries_step == 0:
					print "%d entries processed." % entries

		if len(self.buffer) > 0:
			self.__flush()
			print "%d entries processed." % entries

		ftoctmp.close()
		self.fblock.close()
		self.fout.close()

		print "Data extraction done."
		print "Sorting index..",

		f = open(self.output_toc_tmp)
		list = []
		for line in f:
			list.append(line.strip())

		f.close()

		list.sort()
	
		f = open(self.output_toc, "w")
		for item in list:
			f.write("%s\n" % item)
		f.close()

		os.remove(self.output_toc_tmp)

		print "done."

