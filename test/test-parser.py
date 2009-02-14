#!/usr/bin/env python

import sys
from daluang.parser import Parser

if len(sys.argv) == 1:
	input = sys.stdin
else:
	if sys.argv[1] == '-':
		input = sys.stdin
	else:
		input = open(sys.argv[1])

wiki = ""
for line in input:
	wiki += line

parser = Parser()
html = parser.parse(wiki, 'id')

print html
