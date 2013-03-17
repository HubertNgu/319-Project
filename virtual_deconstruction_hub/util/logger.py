import os
import constants
import logging

from logging.handlers import TimedRotatingFileHandler

LEVELS = { 'CRITICAL' : logging.CRITICAL, 'ERROR' : logging.ERROR,
			'WARNING' : logging.WARNING, 'INFO' : logging.INFO,
			'DEBUG' : logging.DEBUG }

def configure():
	'''
	Configures the root logger with handlers so that
	it propagates down to all of the loggers.
	'''
	logger = logging.getLogger()
	logger.setLevel(logging.DEBUG)
	logger.addHandler(create_stream_handler(constants.STREAM_LEVEL, constants.STREAM_FORMAT))
	logger.addHandler(create_timed_file_handler(constants.FILE_LEVEL, 
		constants.FILE_FORMAT, constants.LOG_FILE_TTL, constants.LOG_FILENAME, constants.LOG_DIRECTORY))


def create_stream_handler(level, format):
	'''
    Creates the stream handler for the logging module
    that outputs log records directly to the console.

    @param level The logging level of the stream handler
    @param format The format of the stream output for each LogRecord

    @return A new StreamHandler
	'''
	stream_handler = logging.StreamHandler()
	stream_handler.setLevel(level)
	stream_handler.setFormatter(logging.Formatter(format))
	return stream_handler


def create_timed_file_handler(level, format, ttl, filename, path):
	'''
	Creates a TimedRotatingFileHandler for the logging module
	that outputs log records to a file. This file will roll over
	given the ttl (time to live) which will create a new log file
	and back up the existing one.

	@param path The path of the log file (e.g. /logs/system.log)
	@param level The logging level of the file handler
	@param format The format of the file output for each LogRecord
	@param ttl The time to live for the the log file before it rolls over

	@return A new TimedRotatingFileHandler
	'''
	# Create all the directories in the path
	print (path.split('/'))
	for directory in path.split('/'):
		if not os.path.exists(directory):
			os.mkdir(directory)

	# Configure the TimedRotatingFileHandler
	file_handler = TimedRotatingFileHandler(path + '/' + filename, ttl)
	file_handler.setLevel(level)
	file_handler.setFormatter(logging.Formatter(format))
	return file_handler

# Used to test this
if __name__ == '__main__':
	configure()
	logger = logging.getLogger(__name__)
	logger.debug('test %s', 'hi')