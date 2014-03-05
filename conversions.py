import exceptions

def toNum (s, default):
    try:
        return int(s)
    except exceptions.ValueError:
	try:
        	return float(s)
	except exceptions.ValueError:
		return float(default)
