from random import randint
import mcq, frq
import json
import os

class Session:
	name: str
	student_id: int
	student_data: list
	student_data_adv: list # TODO remove after tests
	section: int # 0: reading, 1: listening, 2: speaking, 3: writing

	reading: mcq
	listening: mcq
	speaking: frq
	writing: frq

	def __init__(self, student_id: int, name: str):
		self.student_id = student_id
		self.name = name
		self.student_data = []
		self.student_data_adv = [[], []] # TODO remove after tests
		self.section = 0
		self.reading = mcq.MCQ(0)
		self.listening = mcq.MCQ(1)
		os.mkdir(f"student_data/{self.student_id}")

	def initialize_frq(self) -> None:
		self.speaking = frq.FRQ(2)
		self.writing = frq.FRQ(3)

	def export_data(self) -> None:
		data = {
			"Name": self.name,
			"Reading": self.student_data[0],
			"Listening": self.student_data[1],
		}
		with open(f'student_data/{self.student_id}/scores.txt', 'a', encoding="utf-8") as file:
			for i in data:
				file.write(i + ": " + str(data[i]) + '\n')
		with open(f'student_data/{self.student_id}/scores_adv.json', 'a') as file:
			json.dump(self.student_data_adv, file, indent=4)

		

_sessions: dict[str: Session] = {}

def create_session(student_id: int, name: str) -> str:
	# ultra safe guard, you never know if the 1 in 94^100 chance occurs
	while (id := ''.join([chr(randint(0x4E00, 0x9FFF)) for _ in range(100)])) in _sessions: ...
	_sessions[id] = Session(student_id, name)
	return id

# checks if instance exists
def has_session(id: str) -> bool:
	return id in _sessions

# gets an instance 
def get_session(id: str) -> Session:
	return _sessions[id]

def remove_session(id: str) -> None:
	del _sessions[id]