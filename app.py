from flask import Flask, render_template, request, redirect, make_response
import sessions

app = Flask(__name__, static_url_path='', static_folder='')

def get_session() -> sessions: # return specific session
    return sessions.get_session(request.cookies.get('id'))

def has_session() -> bool: # return if user has session
    return sessions.has_session(request.cookies.get('id'))

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
    if not(has_session()): # redirects to home if session not found
        return redirect('/')
    
    sections = {0: ["Reading Multiple-Choice", "Select the option that best responds to the question"], 1: ["Listening Multiple-Choice", "You will listen to a short conversation and select the option that best responds to the question. You will only be able to listen to it once."], 2: ["Speaking Free-Response", "You will be given a prompt to talk about. You will have 4 minutes to prepare, 2 minutes to record. When you are finished, upload the recording here: https://drive.google.com/drive/folders/1EUs8PzMLBB2FlQbryFL8C23s5np8DnNu?usp=drive_link"], 3: ["Writing Free-Response", "You will be given a prompt to write about. You will have 15 minutes to submit"]}

    session = get_session()
    if session.section < 4:
        return render_template('instruction.html', section_name=sections[session.section][0], instructions=sections[session.section][1]) # instructions page based on section
    else:
        session.export_data()
        sessions.remove_session(request.cookies.get('id'))
        return render_template('result.html')
        

@app.route('/continue_test', methods=['POST'])
def continue_test(): # redirect to correct page
    session = get_session()
    match session.section:
        case 0 | 1:
            return redirect("/mcq-question")
        case 2:
            session.initialize_frq() # initialize frqs based on previous thetas
            return redirect("/frq-question")
        case 3:
            return redirect("/frq-question")

# this function will return question page
@app.route('/mcq-question', methods=['GET'])
def create_mcq_question_page():
    if not(has_session()): # redirects to home if session not found
        return redirect('/')
    
    session = get_session()
    match session.section:
        case 0:
            session = session.reading
        case 1:
            session = session.listening

    # check if session needs to stop
    if session.check_stop():
        get_session().section += 1
        get_session().student_data.append(session.theta)
        return redirect('/instruction')
    
    prompt, questions, options = session.get_question() # get question data
    # set question counter (range if multiple questions)
    if len(questions) == 1: questionnumber = len(session.questions_answered)
    else: questionnumber = str(len(session.questions_answered) - len(questions) + 1) + " - " + str(len(session.questions_answered))
    match session.section:
        case 0: 
            return render_template('reading.html', prompt=prompt, questions=questions, options=options, questionnumber=questionnumber)
        case 1:
            return render_template('listening.html', audio=prompt, questions=questions, options=options, questionnumber=questionnumber)

# Route to handle form submission
@app.route('/submit_mcq', methods=['POST'])
def submit_mcq():
    if not(has_session()):
        return redirect('/')
    
    session = get_session()
    match session.section:
        case 0:
            session = session.reading
        case 1:
            session = session.listening

    user_answer = []
    try:
        for i in range(10): # get user response as a list
            user_answer.append(int(request.form.get(str(i))))
    except TypeError:
        pass
    session.answer_question(user_answer) # check answer
    return redirect('/mcq-question')

@app.route('/frq-question', methods=['GET'])
def create_frq_question_page():
    if not(has_session()): # redirects to home if session not found
        return redirect('/')
    
    session = get_session()
    match session.section:
        case 2:
            session = session.speaking
            return render_template('speaking.html', prompt=session.select_prompt())
        case 3:
            session = session.writing
            return render_template('writing.html', prompt=session.select_prompt())

@app.route('/submit-frq', methods=['POST'])
def submit_frq():
    session = get_session()
    session.section += 1
    session.student_data.append(request.form.get("frq"))
    return redirect('/instruction')

if __name__ == '__main__':
    app.run(port=3001, host="0.0.0.0")