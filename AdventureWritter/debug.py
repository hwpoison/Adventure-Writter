
DEBUG_INFO = True

def dprint(*args):
	# debug message print
	if(DEBUG_INFO):
		dmsg = ''.join([str(str_) for str_ in args])
		print(dmsg)
