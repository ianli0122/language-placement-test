import students

class Session:
	...

class _ReadingSession(Session):
	...

class _ListeningSession(Session):
	...

class _SpeakingSession(Session):
	...

class _WritingSession(Session):
	...

def is_session_open(id: str) -> bool:
	...

# gets a new session 
def open_session(id: str) -> (str, Session):

	...