# this is also an imrpoved copy os instances.py

import students

class Session:
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

# gets a new session, returns the SessionID (wrapper for a string) and a Session
# we return SessionID instead of str so we dont get id and session id mixed up
# if the session id is None, that means either the session is open or they are already finished
def open_session(id: str) -> (SessionID, Session):
	if is_session_open(id):
		return None, None
	
	data = students.get_student_data(id)["stage"]

	match data: # TODO create appropiate constructors
		case 0:
			return _ReadingSession()
		case 1:
			return _ListeningSession()
		case 2:
			return _SpeakingSession()
		case 3:
			return _WritingSession()
		case 4, _:
			return None, None