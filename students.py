# this is essentially a copy of the old instances.py

import json

with open("data/student_ids.json", "r") as file:
	_student_ids = json.load(file)

# have to do this just in case the file doesnt exist
def _get_student_data() -> dict:
	try:
		with open("data/student_data.json", "r") as file:
			return json.load(file)
	except FileNotFoundError:
		return {}
	
_student_data = {str(id): { # default data

} for id in _student_ids} | _get_student_data() # this creates defaults for the student data and writes the current student data over it
