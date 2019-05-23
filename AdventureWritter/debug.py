import configparser
import os

# dir_ = os.path.dirname(os.path.abspath(__file__))
debug = configparser.ConfigParser()
debug.read('config.ini')

DEBUG_INFO = True if debug['DEBUG'].getboolean('debug') == 'True' else False

def dprint(*args):
	# debug message print
	if(DEBUG_INFO):
		dmsg = ''.join([str(str_) for str_ in args])
		print(dmsg)
