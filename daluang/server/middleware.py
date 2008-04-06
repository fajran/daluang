
# This code is derived from Django's locale.py (LocaleMiddleware)

from django.utils.cache import patch_vary_headers
from django.utils import translation
#from daluang.server import translation
import locale

class LocaleMiddleware(object):

	def process_request(self, request):
		language = locale.getdefaultlocale()[0]
		translation.activate(language)
		request.LANGUAGE_CODE = translation.get_language()

	def process_response(self, request, response):
		patch_vary_headers(response, ('Accept-Language',))
		response['Content-Language'] = translation.get_language()
		translation.deactivate()
		return response

