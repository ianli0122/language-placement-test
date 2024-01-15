from catsim.initialization import RandomInitializer
from catsim.selection import MaxInfoSelector
from catsim.estimation import NumericalSearchEstimator
from catsim.stopping import *
from catsim.irt import see
import numpy as np
import json
from flask import Flask, render_template, request, redirect, url_for, make_response
import instances

app = Flask(__name__)
selector = MaxInfoSelector()
estimater = NumericalSearchEstimator()

# Route for the home page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# this is the function that gets called when the user presses the "start" button on home.html
# we will be essentially copying this:

@app.route('/start', methods=['POST'])
def start():
    resp = make_response(redirect('/question')) # magic function that gets the user, im not sure if this works
    resp.set_cookie('id', instances.create_instance()) # this will create a cookie named "id" for the user, which can be get later
    return resp

# this function will return question page
@app.route('/question', methods=['GET'])
def create_question_page():
    id = request.cookies.get('id') # gets the id (stored as a cookie)
    instance = instances.get_instance(id)
    
    # check if instance needs to stop
    if instances.check_stop(instance):
        instances.remove_instance(id)
        return render_template('result.html', score=instance.theta)
    
    question, options = instances.get_question_data(instance.start_answering_question())
    return render_template('question.html', question=question, options=options)

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    id = request.cookies.get('id')
    instance = instances.get_instance(id)
    user_answer = request.form.get('answer')
    instance.answer_question(user_answer)
    return redirect('/question')