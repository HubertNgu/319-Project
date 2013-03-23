from ast import literal_eval
from ConfigParser import RawConfigParser

def load(path):
	'''
    Loads a file given a path. Stores all of the variables in the
    globals() dict for the constants.py file.
	'''
	config = RawConfigParser()
	config.read(path)

	sections = config.sections()

	for section in sections:
		print section
		for key, value in config.items(section):
			print key.upper(), value
			try:
				globals()[key.upper()] = literal_eval(value)
			except:
				globals()[key.upper()] = value

# Used to test this
if __name__ == '__main__':
	load('config/default.cfg')
	print globals()
	print stream_format