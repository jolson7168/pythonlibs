import exceptions

def toNum (s):
    try:
        return int(s)
    except exceptions.ValueError:
	try:
        	return float(s)
	except exceptions.ValueError:
		return float(config["noVal"])
