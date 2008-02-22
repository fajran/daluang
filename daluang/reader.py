#!/usr/bin/python

import bz2
import os

class Reader:

	def __init__(self, index_file, toc_file, block_file):
		self.index_file = index_file
		self.toc_file = toc_file
		self.block_file = block_file

		self.blocks = { }

		f = open(self.block_file)
		for line in f:
			p = line.strip().split(" ")
			self.blocks[int(p[0])] = [int(p[1]), int(p[2])]
		f.close()

	def get_block(self, block):
		block_start = self.blocks[block][0]
		block_length = self.blocks[block][1]
		return block_start, block_length

	def read_data(self, block_start, block_length, offset, length):
		
		f = open(self.index_file)
		f.seek(block_start)
		data = f.read(block_length)
		f.close()

		f = open('/tmp/test', 'w')
		f.write(data)
		f.close()

		end = offset + length
		data = bz2.decompress(data)
		data = data[offset:end]

		pos = data.index("\n")
		title = data[0:pos]
		content = data[pos+1:]

		return title, content
	
	def read(self, title):
		loc = self.find(title)
		if loc == None:
			return None

		block, offset, length = loc

		block_start, block_length = self.get_block(block)

		return self.read_data(block_start, block_length, offset, length)

	def find(self, title):
	
		offset = -1
		length = -1

		title = title.lower().replace('_', ' ')
	
		f = open(self.toc_file)
		f.seek(0, 2)
		size = f.tell()

		low = 0
		high = size
		pos = size / 2

		# Binary search
		while True:
			f.seek(pos)
			f.readline()
			pos = f.tell()
			line = f.readline()
			line = line.strip().lower()

			p = line.split("\t")

			if p[0] == title:
				block = int(p[1])
				offset = int(p[2])
				length = int(p[3])
				break

			elif p[0] < title:
				low = pos - 100
				pos = (low + high) / 2
			else:
				high = pos + 100
				pos = (low + high) / 2

			if high - low < 2048:
				low = low - 1024
				if low < 0:
					low = 0
					
				f.seek(low)
				f.readline()
				cnt = 0
				while f.tell() <= high:
					p = f.tell()
					line = f.readline()
					if line == '':
						break

					line = line.strip().lower()
					p = line.split("\t")
		
					if p[0] == title:
						block = int(p[1])
						offset = int(p[2])
						length = int(p[3])
						break

				break
					
		f.close()
	
		if offset == -1:
			return None

		return block, offset, length

