from catsim.selection import MaxInfoSelector
from catsim.estimation import NumericalSearchEstimator
from catsim.stopping import MaxItemStopper, MinErrorStopper
from catsim.initialization import RandomInitializer
from random import randint
import numpy as np
import json
import csv

class Instance:
	theta: float
	questions_answered: list[int]
	responses: list[bool]
	student_id: int

	# these are variables for storing data about the next question
	question_answer: any

	# do not use this, use create_instance()
	def __init__(self):
		self.theta = RandomInitializer("uniform", (-0.5, 0.5)).initialize()
		self.questions_answered = []
		self.responses = []
		self.student_id = -1
	
	def __repr__(self) -> str:
		return f'Instance[theta={self.theta}, questions_answered={self.questions_answered}, responses={self.responses}, student_id={self.student_id}]'
	
	def set_student_id(self, student_id: int):
		self.student_id = student_id

	def start_answering_question(self) -> int:
		print(_instance_dict)
		question_index, correct_answer = select_question(self) # get question
		self.questions_answered.append(question_index)
		self.question_answer = correct_answer
		return question_index

	# accepts the answers, returns whether or not they answered correct along with the level
	def answer_question(self, answer: str):
		self.responses.append(self.question_answer == answer)
		self.theta = calc_new_theta(self) 

# generates a random 100 char string
def generate_id() -> str:
	return ''.join([chr(randint(0x4E00, 0x9FFF)) for _ in range(100)])

_instance_dict: dict[str: Instance] = {}

# methods

# creates a new instance, and returns the instance ID
def create_instance() -> str:
	# ultra safe guard, you never know if the 1 in 94^100 chance occurs
	while (id := generate_id()) in _instance_dict: ...
	_instance_dict[id] = Instance()
	return id

# gets an instance 
def get_instance(id: str) -> Instance:
	return _instance_dict[id]

def remove_instance(id: str) -> None:
	del _instance_dict[id]

_selector = MaxInfoSelector()
_estimater = NumericalSearchEstimator()
_item_stopper = MaxItemStopper(20)
_error_stopper = MinErrorStopper(0.8)

#Import questions file, format to compatible numpy array
with open("questions.json", encoding="utf8") as questionFile:
    _questions: list[(str, int, list[str], str)] = list(map(tuple, json.load(questionFile)))
    
# parse questions into something else that the library understands
_questions_np = np.array([[1, level, 1 / len(answers), 1] for _, level, answers, _ in _questions])

def get_question_data(index: int) -> (str, list[str]):
    return _questions[index][0], _questions[index][2]

# this will be called from instance
def select_question(instance: Instance) -> (int, str):
    question_number = _selector.select(None, _questions_np, instance.questions_answered, instance.theta)
    return question_number, _questions[question_number][3] # returns index and correct answer

def check_stop(instance: Instance) -> bool:
	questions_answered_np = np.array([arr for i, arr in enumerate(_questions_np) if i in instance.questions_answered])
	return _item_stopper.stop(None, questions_answered_np) or len(instance.questions_answered) > 5 and _error_stopper.stop(None, questions_answered_np, instance.theta)

def calc_new_theta(instance: Instance):
    return _estimater.estimate(None, _questions_np, instance.questions_answered, instance.responses, instance.theta)

def export_data(instance: Instance):
	with open("scores.csv", mode='a', newline='') as file:
		csv.writer(file).writerow([instance.student_id, instance.theta])