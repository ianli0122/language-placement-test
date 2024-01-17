# script for generating dummy questions for testing. 
# usage: python generate.py (mcq|frq)

import sys, json, random

def generate_mcq() -> None:
	questions = []

	# generate 30 single-reading questions
	for i in range(30):
		difficulty = random.randint(1, 5)
		questions.append({
			"type": "single-reading",
			"text": f"Q{i + 1} text",
			"difficulty": difficulty,
			"question": f"single-reading Q{i + 1} difficulty={difficulty} question",
			"options": ["a", "b", "c"],
			"correct": 0 # correct answer will always be "a"
		})

	# generate 20 multi-reading questions
	for i in range(20):
		difficulty = random.randint(1, 5)
		questions.append({
			"type": "multi-reading",
			"text": f"multi-reading Q{i + 1} difficulty={difficulty}",
			"difficulty": difficulty,
			"questions": [
				{
					"question": f"multi-reading Q{i + 1}.{j + 1} question",
					"options": ["a", "b", "c"],
					"correct": 0 # correct answer is always a
				} for j in range(random.randint(3, 6)) # generates a random number of additional questions for each mutli question
			]
		})
	
	# generate 30 single-listening questions
	for i in range(10):
		difficulty = random.randint(1, 5)
		audio_num = random.randint(1, 4)
		questions.append({
			"type": "single-listening",
			"audio": f"audio{audio_num}.wav",
			"difficulty": difficulty,
			"question": f"single-reading Q{i + 1} difficulty={difficulty}",
			"options": ["a", "b", "c"],
			"correct": 0 # correct answer will always be "a"
		})

	# generate 30 multi-listening questions
	for i in range(20):
		difficulty = random.randint(1, 5)
		audio_num = random.randint(1, 4)
		questions.append({
			"type": "multi-listening",
			"audio": f"audio{audio_num}.wav",
			"text": f"multi-reading Q{i + 1} difficulty={difficulty}",
			"questions": [
				{
					"question": f"multi-reading Q{i + 1}.{j + 1}",
					"options": ["a", "b", "c"],
					"correct": 0 # correct answer is always a
				} for j in range(random.randint(3, 6)) # generates a random number of additional questions for each mutli question
			]
		})

	# shuffle array so that we can test
	# not really necessary 
	# random.shuffle(questions)

	with open("mcq.json", "w") as file:
		json.dump(questions, file)

def generate_frq() -> None:
	...

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print(f"Invalid number of parameters. (1 required, {len(sys.argv) - 1} found)")
		sys.exit(1)
	elif "mcq" in sys.argv:
		print("generating mcq.json...")
		generate_mcq()
	elif "frq" in sys.argv:
		print("generating frq.json...")
		generate_frq()
	else:
		print(f"Second argument must be 'mcq' or 'frq'. ({sys.argv[1]} found)")
		sys.exit(1)