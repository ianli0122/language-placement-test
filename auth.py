# a file to handle authentications (admin, student password, etc)

import random, dotenv

_dotenv = dotenv.dotenv_values()

_admin_password_hash = hash(_dotenv["ADMIN_PASSWORD"]) # probably shouldnt directly store admin password, should also probably not store this in .env (store as hash)
_salt = _dotenv["SALT"]

def is_admin_password(password: str) -> bool:
	return hash(password) == _admin_password_hash

