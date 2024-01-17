# script for generating dummy questions for testing. 
# usage: python generate.py (mcq|frq)

import sys

def generate_mcq() -> None:
	...

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
