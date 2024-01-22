from flask import Flask, render_template, request, redirect, make_response
import sessions

app = Flask(__name__)

# return specific session
def get_session() -> sessions:
    return sessions.get_session(request.cookies.get('id'))

# home page
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

# start button
@app.route('/start', methods=['POST'])
def start():
    resp = make_response(redirect('/instruction')) # redirects users
    id = sessions.create_session(request.form.get('student_id'))
    resp.set_cookie('id', id) # this will create a cookie named "id" for the user, which can be get later
    return resp

@app.route('/instruction', methods=['GET'])
def instructions():
    sections = {0: ["Reading Multiple-Choice", "instructions go here"], 1: ["Listening Multiple-Choice", "instructions"], 3: ["Speaking Free-Response", "instructions"], 4: ["Writing Free-Response", "instructions"]}
    session = get_session()
    return render_template('instruction.html', section_name=sections[session.section][0], instructions=sections[session.section][1])

@app.route('/continue_test', methods=['POST'])
def continue_test():
    session = get_session()
    print(session.section)
    match session.section:
        case 0 | 1:
            return make_response(redirect("/mcq-question"))

# this function will return question page
@app.route('/mcq-question', methods=['GET'])
def create_mcq_question_page():
    id = request.cookies.get('id') # gets the id (stored as a cookie)
    if not(sessions.has_session(id)): # redirects to home if session not found
        return redirect('/')
    
    session = get_session()
    match session.section:
        case 0:
            session = session.reading
        case 1:
            session = session.listening

    # check if session needs to stop
    if session.check_stop():
        sessions.remove_session(id)
        return render_template('result.html')
    
    global questions
    prompt, questions, options = session.get_question() # get question data
    # set question counter (range if multiple questions)
    if len(questions) == 1: questionnumber = len(session.questions_answered)
    else: questionnumber = str(len(session.questions_answered) - len(questions) + 1) + " - " + str(len(session.questions_answered))
    return render_template('mcq-question.html', prompt=prompt, questions=questions, options=options, questionnumber=questionnumber)

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    session = get_session()
    user_answer = []
    for i in range(len(questions)): # get user response as a list
        user_answer.append(int(request.form.get(str(i))))
    session.reading.answer_question(user_answer) # check answer
    return redirect('/mcq-question')

if __name__ == '__main__':
    app.run(port=3001, host="0.0.0.0", debug=True)