
__all__ = ['load_languages']

def load_languages(fname):
	f = open(fname)

	languages = {}

	for line in f:
		line = line.strip()
		if line[0] == '#':
			continue

		(code, language) = line.split("\t")
		languages[code] = language

	return languages

