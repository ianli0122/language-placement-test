import json

class FRQ:
    response: str
    theta: float
    section: int # 0: speaking, 1: writing

    def __init__(self, theta: float, section: int):
        question_vars("sfrq")
        question_vars("wfrq")
        self.theta = theta
        self.section = section - 2
    
    def select_prompt(self) -> str:
        score = round(self.theta)
        if score < 1:
            score = 1
        elif score > 5:
            score = 5

        return _questions[self.section][str(score)]


_questions: list[dict] = []
def question_vars(file: str) -> None:
    with open(f"data/{file}.json", 'r', encoding="utf8") as questionFile:
        _questions.append(json.load(questionFile))