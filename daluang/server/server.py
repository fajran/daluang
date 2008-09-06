#!/usr/bin/python

#import os
#from django.core.servers import basehttp
#from django.core.handlers import wsgi
#
#def start(settings="daluang.server.settings", addr="127.0.0.1", port=8000):
#	os.environ['DJANGO_SETTINGS_MODULE'] = settings
#	handler = wsgi.WSGIHandler()
#
#	try:
#		basehttp.run(addr, port, handler)
#	except KeyboardInterrupt:
#		pass
	
from BaseHTTPServer import HTTPServer
from handler import DaluangHandler

def start(addr="127.0.0.1", port=8000):
	server = HTTPServer((addr, port), DaluangHandler)
	server.serve_forever()

