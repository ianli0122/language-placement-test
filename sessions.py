# this is also an imrpoved copy os instances.py

import students
from random import randint
from abc import abstractmethod
from typing import Self

class Session:
	_data: dict[str]

	def __init__(self, data: dict[str]):
		self._data = data
		

	@abstractmethod
	def advance() -> bool:
		...

	@abstractmethod
	def next_session() -> Self:
		...
	
	@abstractmethod
	def render() -> str:
		...

class SessionID(str): ...

class _ReadingSession(Session):
	...

class _ListeningSession(Session):
	...

class _SpeakingSession(Session):
	...

class _WritingSession(Session):
	...

def is_session_open(id: str) -> bool:
	return students.get_student_data(id)["in-session"]

def _generate_session_id() -> SessionID:
	return SessionID(''.join([chr(randint(0x4E00, 0x9FFF)) for _ in range(100)]))

# gets a new session, returns the SessionID (wrapper for a string) and a Session
# we return SessionID instead of str so we dont get id and session id mixed up
# if the session id is None, that means either the session is open or they are already finished
def open_session(id: str) -> (SessionID, Session):	
	data = students.get_student_data(id)
	if not(data["in-session"]) or data["stage"] == 4:
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