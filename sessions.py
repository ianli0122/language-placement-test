from random import randint
import mcq, frq
import json
import os

class Session:
	name: str
	student_id: int
	student_data: list
	student_data_adv: list # TODO remove after tests
	section: int # 0: reading, 1: listening, 2: speaking, 3: writing computer, 4: writing paper

	reading: mcq
	listening: mcq
	free_response: frq
	writing_prompt: int # index of typed prompt given

	def __init__(self, student_id: int, name: str):
		self.student_id = student_id
		self.name = name
		self.student_data = []
		self.student_data_adv = [[], []] # TODO remove after tests
		self.section = 0
		self.reading = mcq.MCQ(0)
		self.listening = mcq.MCQ(1)
		self.free_response = frq.FRQ()
		os.mkdir(f"student_data/{self.student_id}")

	def export_data(self) -> None:
		data = {"Name": self.name}
		if self.section >= 1: data["Reading"] = self.student_data[0]
		if self.section >= 2: data["Listening"] = str(self.student_data[1]) + "\n\n"
		if self.section >= 4: 
			data["Writing Prompt"] = json.load(open("question_data/wfrq.json", 'r', encoding="utf-8"))[self.writing_prompt]
			data["Writing"] = self.student_data[2]
		with open(f'student_data/{self.student_id}/scores.txt', 'w', encoding="utf-8") as file:
			for i in data:
				file.write(i + ": " + str(data[i]) + '\n')
		with open(f'student_data/{self.student_id}/scores_adv.json', 'w') as file: # TODO remove after tests
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