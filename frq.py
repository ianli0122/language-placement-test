import json
from random import randint

class FRQ:
    response: str
    selectedPrompts: list[int]

    def __init__(self):
        question_vars("sfrq")
        question_vars("wfrq")
        self.selectedPrompts = []
        for i in range(3):
            if i <= 1:
                self.selectedPrompts.append(randint(0, len(_questions[i]) - 1))
            else:
                self.selectedPrompts.append(randint(0, len(_questions[1]) - 1))
        while self.selectedPrompts[1] == self.selectedPrompts[2]:
            self.selectedPrompts[2] = randint(0, len(_questions[1]) - 1)
    
    def select_prompt(self, section: int) -> tuple[str, int]: # returns prompt, typed prompt index
        section -= 2
        if section == 0:
            return _questions[section][self.selectedPrompts[section]], -1
        elif section == 1:
            return _questions[section][self.selectedPrompts[section]], self.selectedPrompts[section]
        elif section == 2:
            return _questions[1][self.selectedPrompts[2]], -1

_questions: list = []
def question_vars(file: str) -> None:
    with open(f"question_data/{file}.json", 'r', encoding="utf8") as questionFile:
        _questions.append(json.load(questionFile))