# a file to handle authentications (admin, student password, etc)

import random as _random, dotenv as _dotenv

_dotenv = _dotenv.dotenv_values()

_admin_password_hash = hash(_dotenv["ADMIN_PASSWORD"]) # probably shouldnt directly store admin password, should also probably not store this in .env (store as hash)
_salt = _dotenv["SALT"]

def is_admin_password(password: str) -> bool:
	return hash(password) == _admin_password_hash

def _gen_password(seed: int) -> str:
	generator = _random.Random(seed)
	choices = [*range(33, 65), *range(97, 123), *range(97, 123)]
	return "".join([chr(generator.choice(choices)) for _ in range(10)])

def get_student_password(id: int) -> str:
	return _gen_password(hash(str(id) + _salt))

def check_student_password(id: int, password: str) -> bool:
	return get_student_password(id) == password