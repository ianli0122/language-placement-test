from flask import Flask, render_template, request, redirect, make_response
import instances

app = Flask(__name__)

# Route for the home page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# this is the function that gets called when the user presses the "start" button on home.html
# we will be essentially copying this:

@app.route('/start', methods=['POST'])
def start():
    resp = make_response(redirect('/question')) # redirects users
    id = instances.create_instance()
    resp.set_cookie('id', id) # this will create a cookie named "id" for the user, which can be get later
    instances.get_instance(id).set_student_id(request.form.get('student_id')) # sets student id
    return resp

# this function will return question page
@app.route('/question', methods=['GET'])
def create_question_page():
    id = request.cookies.get('id') # gets the id (stored as a cookie)

    if not instances.has_instance(id):
        return redirect('/')

    instance = instances.get_instance(id)
    
    # check if instance needs to stop
    if instances.check_stop(instance):
        instances.export_data(instance)
        instances.remove_instance(id)
        return render_template('result.html')
    
    instruction, questions, options = instances.get_question_data(instance.start_answering_question())
    return render_template('question.html', instruction=instruction, questions=questions, options=options, questionnumber = len(instance.questions_answered)) # TODO small bug here with paragraph questions, automatically skips to # of last question

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    id = request.cookies.get('id')
    instance = instances.get_instance(id)
    user_answer = request.form.get('answer')
    instance.answer_question(user_answer)
    return redirect('/question')

if __name__ == '__main__':
    app.run(port=3001, host="0.0.0.0")