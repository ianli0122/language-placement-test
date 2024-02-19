from catsim.selection import MaxInfoSelector
from catsim.estimation import NumericalSearchEstimator
from catsim.stopping import MaxItemStopper, MinErrorStopper
from random import random
import numpy as np
import json

# catsim variables
_selector = MaxInfoSelector()
_estimater = NumericalSearchEstimator()
_item_stopper = MaxItemStopper(20)
_error_stopper = MinErrorStopper(0.6)

class MCQ:
    theta: float
    questions_answered: list[int]
    responses: list[bool]
    question_answers: list[int]
    section: int # 0 is reading, 1 is listening

    def __init__(self, section: int):
        self.theta = random() + 1 # generate float between 1-2
        self.questions_answered = []
        self.responses = []
        self.section = section
        # initialize question bank variables
        question_vars("rmcq")
        question_vars("lmcq")

    def get_question(self) -> tuple[str, list[str], list[list[str]]]: # returns question prompt, questions, and options
        index, self.question_answers = select_question(self)
        questions, selections = [], []
        for i in index:
            self.questions_answered.append(i)
            questions.append(_questions[self.section][i][1])
            selections.append(_questions[self.section][i][3])
        return _questions[self.section][index[0]][0], questions, selections
    
    def answer_question(self, answer: list[int]):
        for i in range(len(answer)): self.responses.append(answer[i] == self.question_answers[i]) # append bools to responses
        self.theta = calc_new_theta(self) # calculate new theta

    def check_stop(self) -> bool: # returns a bool whether to stop or not
        questions_answered_np = np.array([arr for i, arr in enumerate(_questions_np[self.section]) if i in self.questions_answered])
        try:
            return _item_stopper.stop(None, questions_answered_np) or len(self.questions_answered) > 5 and _error_stopper.stop(None, questions_answered_np, self.theta)
        except ValueError:
            return True


# question database initialization
_questions: list[list[str, str, int, list[str], int]] = [] # list[prompt: str, question: str, diff: int, selection: list[str], correct: int]
_connected_questions: list[list[list[int]]] = [] # list[list[int]] connected questions
_questions_np: list[any] = []
def question_vars(file: str) -> None:
    with open(f"question_data/{file}.json", 'r', encoding="utf8") as questionFile:
        questions: list[str, str, int, list[str], int]= []
        connected_questions: list[list[int]] = []
        for i in json.load(questionFile):
            if type(i["question_data"]) == dict: # check if connected questions
                questions.append([i["prompt"], i["question_data"]["question"], i["difficulty"], i["question_data"]["options"], i["question_data"]["correct"]])
            else:
                connected_question = [] # temp var to store grouped problem
                for q in i["question_data"]:
                    connected_question.append(len(questions)) # append index
                    questions.append([i["prompt"], q["question"], i["difficulty"], q["options"], q["correct"]]) # append to main questions list
                connected_questions.append(connected_question) # append indexes to connected questions
    _questions.append(questions)
    _connected_questions.append(connected_questions)
    _questions_np.append(np.array([[1, level, 1 / len(answers), 1] for _, _, level, answers, _ in questions]))


def select_question(mcq: MCQ) -> tuple[list[int], list[int]]: # select question based on theta, return list of question indexes and answers
    question_number = _selector.select(None, _questions_np[mcq.section], mcq.questions_answered, mcq.theta) # algorithm selects question index
    for i in _connected_questions[mcq.section]:
        if question_number in i: # check if index in _connected_questions
            indexes = i 
            answer = []
            for q in i:
                answer.append(_questions[mcq.section][q][4])
            return indexes, answer # return list of indexes, answers
    return [question_number], [_questions[mcq.section][question_number][4]] # else, return a single index and answer

def calc_new_theta(mcq: MCQ): # calculate new theta
    return _estimater.estimate(None, _questions_np[mcq.section], mcq.questions_answered, mcq.responses, mcq.theta)