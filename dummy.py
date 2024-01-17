# script for generating dummy questions for testing. 
# usage: python dummy.py

import sys, json, random
from typing import Callable

_func_dict: dict[str: dict[str: any]] = {}

# decorator for generation functions
def _data_function(name: str, desc: str = None):
	desc = f'Generates {name}.json.' if desc is None else desc
	def wrapper(func: Callable[[], list | dict]):
		_func_dict[name] = {
			"desc": desc,
			"func": func
		}
		return func
	return wrapper

# reading multiple choice questions
@_data_function("rmcq", "Generates rmcq.json, a file containing dummy reading multiple choice questions.")
def _gen_rmcq() -> list:
	questions = []

	# generate 30 single reading questions
	for i in range(30):
		difficulty = random.randint(1, 5)
		questions.append({
			"type": "reading",
			"text": f"reading Q{i + 1} difficulty={difficulty} single question text",
			"difficulty": difficulty,
			"question_data": {
				"question": f"reading Q{i + 1} question",
				"options": ["a", "b", "c"],
				"correct": 0 # correct answer will always be "a"
			}
		})

	# generate 20 multi reading questions
	for i in range(20):
		difficulty = random.randint(1, 5)
		questions.append({
			"type": "reading",
			"text": f"reading Q{i + 1} difficulty={difficulty} multi question text",
			"difficulty": difficulty,
			"questions": [
				{
					"question": f"reading Q{i + 1}.{j + 1} question",
					"options": ["a", "b", "c"],
					"correct": 0 # correct answer is always a
				} for j in range(random.randint(3, 6)) # generates a random number of additional questions for each mutli question
			]
		})
	
	# shuffle array so that we can test
	# not really necessary 
	# random.shuffle(questions)

	return questions

# listening multiple choice questions
@_data_function("lmcq", "Generates lmcq.json, a file containing dummy listening multiple choice questions.")
def _gen_lmcq() -> list:
	questions = []

	# generate 30 single listening questions
	for i in range(30):
		difficulty = random.randint(1, 5)
		audio_num = random.randint(1, 4)
		questions.append({
			"type": "listening",
			"audio": f"audio{audio_num}.wav",
			"difficulty": difficulty,
			"question_data": {
				"question": f"listening Q{i + 1} difficulty={difficulty} audio={audio_num} single question",
				"options": ["a", "b", "c"],
				"correct": 0 # correct answer will always be "a"
			}
		})

	# generate 20 multi listening questions
	for i in range(20):
		difficulty = random.randint(1, 5)
		audio_num = random.randint(1, 4)
		questions.append({
			"type": "listening",
			"audio": f"audio{audio_num}.wav",
			"difficulty": difficulty,
			"questions": [
				{
					"question": f"listening Q{i + 1}.{j + 1} difficulty={difficulty} audio={audio_num} multi question",
					"options": ["a", "b", "c"],
					"correct": 0 # correct answer will always be "a"
				} for j in range(random.randint(3, 6)) # generates a random number of additional questions for each mutli question
			]
		})
	
	return questions

# writing prompts
@_data_function("wfrq", "Generates wfrq.json, a file containing dummy writing free response questions.")
def _gen_wfrq() -> dict:
	return {str(i): [f"writing prompt {j + 1} difficulty={i}" for j in range(3)] for i in range(1, 6)}

# speaking prompts
@_data_function("sfrq", "Generates sfrq.json, a file containing dummy speaking free response questions.")
def _gen_sfrq() -> dict:
	return {str(i): [f"speaking prompt {j + 1} difficulty={i}" for j in range(3)] for i in range(1, 6)}

def _print_help() -> None:
	print("Generator for dummy data for this project.")
	print(f"Usage: python dummy.py (OPTION)\n\nOptions:")
	print("\n".join([f"  {k} - {v["desc"]}" for k, v in _func_dict.items()]))
	print("  help - Prints this help page.")
	print("  all - Generates all files. Refer to above.")

if __name__ == "__main__":
	special = ["all", "help"]

	if len(sys.argv) != 2 or sys.argv[1] not in _func_dict and sys.argv[1] not in special:
		_print_help()
		sys.exit(1)
	elif sys.argv[1] == "help":
		_print_help()
		sys.exit(0)
	elif sys.argv[1] == "all":
		# TODO
		sys.exit(0)
	