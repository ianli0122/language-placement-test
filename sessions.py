from random import randint
import mcq
import json

class Session:
	student_id: int
	student_data: dict
	section: int # 0: reading, 1: listening, 2: speaking, 3: writing
	reading: mcq
	listening: mcq

	def __init__(self, student_id: int):
		self.student_id = student_id
		self.student_data = {
			"section": 0,
			"active": True,
			"reading": None,
			"listening": None,
			"speaking": None,
			"writing": None
		}
		self.section = 0
		self.reading = mcq.MCQ(0)
		self.listening = mcq.MCQ(1)
		

_sessions: dict[str: Session] = {}

def create_session(student_id: int) -> str:
	# ultra safe guard, you never know if the 1 in 94^100 chance occurs
	while (id := ''.join([chr(randint(0x4E00, 0x9FFF)) for _ in range(100)])) in _sessions: ...
	_sessions[id] = Session(student_id)
	return id

# checks if instance exists
def has_session(id: str) -> bool:
	return id in _sessions

# gets an instance 
def get_session(id: str) -> Session:
	return _sessions[id]

def remove_session(id: str) -> None:
	del _sessions[id]

def next_section(id: str) -> None:
	_sessions[id].student_data["section"] += 1