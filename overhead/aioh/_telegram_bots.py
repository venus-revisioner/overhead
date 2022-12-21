
class _kerttulibot:
	"""
	print(_kerttulibot.TOKEN)
	"""
	_key_path = "D:\\OVERHEAD_PY\\TOKEN_KERTTULIBOT.txt"
	with open(_key_path, "r") as f:
		_token = f.read()
		_token = _token.strip()
		_token = _token.strip("\n")
		_token = _token.strip("\r")
		_token = _token.strip("\t")
		TOKEN = _token
