import json
from random import randint

class FRQ:
    response: str
    section: int # 0: speaking, 1: writing

    def __init__(self, section: int):
        question_vars("sfrq")
        question_vars("wfrq")
        self.section = section - 2
    
    def select_prompt(self) -> str:
        return _questions[self.section][randint(0, len(_questions[self.section]) - 1)]


_questions: list = []
def question_vars(file: str) -> None:
    with open(f"question_data/{file}.json", 'r', encoding="utf8") as questionFile:
        _questions.append(json.load(questionFile))