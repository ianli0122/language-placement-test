"""
this is essentially an attempt improvement of instances.py

there are several stages
	stage 0 = reading
	stage 1 = listening
	stage 2 = recording
	stage 3 = writing
	stage 4 = finished
"""

import json, random

with open("data/student_ids.json", "r") as file:
	_student_ids: list[int] = json.load(file)

# have to do this just in case the file doesnt exist
def _get_student_data() -> dict:
	try:
		with open("data/student_data.json", "r") as file:
			return json.load(file)
	except FileNotFoundError:
		return {}

_student_data: dict[str: dict[str: any]] = {k: v
	for k, v in ({str(id): { # default data
		"stage": 0, # stage
		"reading": {
			"score": random.random() + 1, # theta
			"answered": [], # questions answered
			"correct": [] # questions correct
		},
		"listening": {
			"score": random.random() + 1,
			"answered": [],
			"correct": []
		},
		"recording": {
			"level": "",
			"prompt": 0,
			"response": ""
		},
		"writing": {
			"level": "",
			"prompt": 0,
			"response": ""
		}
	} for id in _student_ids} | _get_student_data()).items() # this creates defaults for the student data and writes the current student data over it
	if int(k) in _student_ids
}