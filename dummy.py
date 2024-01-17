# script for generating dummy questions for testing. 
# usage: python generate.py (mcq|frq)

import sys, json, random

def generate_rmcq() -> None:
	print("generating rmcq.json...")
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

	with open("rmcq.json", "w") as file:
		json.dump(questions, file)

def generate_lmcq() -> None:
	print("generating lmcq.json...")
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
	
	with open("lmcq.json", "w") as file:
		json.dump(questions, file)


def generate_frq() -> None:
	print("generating frq.json...")
	with open("frq.json", "w") as file:
		json.dump({str(i): [f"FRQ prompt {j + 1} difficulty={i}" for j in range(5)] for i in range(1, 6)}, file)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print(f"Invalid number of parameters. (1 required, {len(sys.argv) - 1} found)")
		sys.exit(1)
	elif "rmcq" in sys.argv:
		generate_rmcq()
	elif "lmcq" in sys.argv:
		generate_lmcq()
	elif "frq" in sys.argv:
		generate_frq()
	elif "all" in sys.argv:
		generate_rmcq()
		generate_lmcq()
		generate_frq()
	else:
		print(f"Second argument must be 'lmcq', 'rmcq', 'frq', or 'all'. ({sys.argv[1]} found)")
		sys.exit(1)