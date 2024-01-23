from random import randint
import mcq, frq
import json

class Session:
	student_id: int
	student_data: list
	section: int # 0: reading, 1: listening, 2: speaking, 3: writing

	reading: mcq
	listening: mcq
	speaking: frq
	writing: frq

	def __init__(self, student_id: int):
		self.student_id = student_id
		self.student_data = []
		self.section = 0
		self.reading = mcq.MCQ(0)
		self.listening = mcq.MCQ(1)

	def initialize_frq(self) -> None:
		self.speaking = frq.FRQ(self.student_data[1], 2)
		self.writing = frq.FRQ(self.student_data[0], 3)

	def export_data(self) -> None:
		data = {
				"reading": self.student_data[0],
				"listening": self.student_data[1],
				"speaking": self.student_data[2],
				"writing": self.student_data[3]
		}
		json.dump({**json.load(open('data/student_data.json')), str(self.student_id): data}, open('data/student_data.json', 'w'), indent=2)
		

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