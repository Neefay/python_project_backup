def read_json(file):
	import json
	with open(file) as f:
		return json.load(f)