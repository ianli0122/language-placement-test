# this is also an imrpoved copy os instances.py

import students, json, random
from abc import abstractmethod
from typing import Self

# get json data

def _get_file(file: str) -> list | dict:
	with open(file, "r") as file:
		return json.load(file)
	
_rmcqs: list[dict[str: any]] = _get_file("data/rmcq.json")
_lmcqs: list[dict[str: any]] = _get_file("data/lmcq.json")
_sfrqs: dict[str: list[str]] = _get_file("data/sfrq.json")
_wfrqs: dict[str: list[str]] = _get_file("data/wfrq.json")

# session classes

class Session:
	...

class SessionID(str): ...

class _Session:
	...

class _ReadingSession(_Session):
	_data_dict: dict[str: any]

	def __init__(self):
		...	

class _ListeningSession(_Session):
	...

class _SpeakingSession(_Session):
	...

class _WritingSession(_Session):
	...

def is_session_open(id: str) -> bool: # NOTE do we still need this?
	return students.get_student_data(id)["in-session"]

def _generate_session_id() -> SessionID:
	return SessionID(''.join([chr(random.randint(0x4E00, 0x9FFF)) for _ in range(100)]))

# gets a new session, returns the SessionID (wrapper for a string) and a Session
# we return SessionID instead of str so we dont get id and session id mixed up
# if the session id is None, that means either the session is open or they are already finished
# TODO fix this so it sends a correct instance and stuff
def open_session(id: str) -> (SessionID, Session):	
	data = students.get_student_data(id)
	if data["in-session"] or data["stage"] == 4:
		return None, None 
	
	session_id = _generate_session_id()
	match data: # TODO create appropiate constructors
		case 0:
			return session_id, _ReadingSession()
		case 1:
			return session_id, _ListeningSession()
		case 2:
			return session_id, _SpeakingSession()
		case 3:
			return session_id, _WritingSession()