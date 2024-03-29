from flask import Flask, render_template, request, redirect, make_response, abort
from werkzeug.serving import make_server
from os.path import splitext
from time import time, localtime
import logging
import sessions

app = Flask(__name__)
allow_connections = False
timeformat = localtime(time())
logging.basicConfig(filename=f'data/logs/{timeformat.tm_year}-{timeformat.tm_mon}-{timeformat.tm_mday}-{timeformat.tm_hour}-{timeformat.tm_min}-{timeformat.tm_sec}.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(name)s: %(message)s', encoding="utf-8")

@app.before_request
def check_active():
    if not allow_connections:
        return "Test not started"

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
    try:
        id = sessions.create_session(request.form.get('student_id'), request.form.get('name'))
        resp.set_cookie('id', id) # this will create a cookie named "id" for the user, which can be get later
    except FileExistsError:
        app.logger.warning(f"Student already exists ({request.form.get("student_id")})")
        return "student already exists"
    return resp

@app.route('/instruction', methods=['GET'])
def instructions():
    if not(has_session()): # redirects to home if session not found
        app.logger.warning(f"{request.cookies.get('id')}: No session detected, redirecting home")
        return redirect('/')
    
    sections = {
        0: ["Reading Multiple-Choice", "Read the question and select the option that best responds to the question."],
        1: ["Listening Multiple-Choice", "You will listen to a short conversation and select the option that best responds to the question. You will only be able to listen to the recording once."],
        2: ["Speaking Free-Response", "You will be given a prompt to talk about in Chinese. You will have 4 minutes to prepare and 2 minutes to record. Please use a recording software (e.g. Voice Memos, www.vocaroo.com) and save the recording. You will be able to upload it on the next page."],
        3: ["Writing Free-Response", "You will be given a prompt to write about. Answer the prompt in the text box thoroughly and thoughtfully."],
        4: ["Writing Free-Response", "You will be given a prompt to write about. Using the paper provided, write down the prompt and answer it thoroughly and thoughtfully in Chinese."]
    }

    session = get_session()
    if session.section < 5:
        app.logger.info(f"{session.student_id}: redirecting to section {session.section}")
        return render_template('instruction.html', section_name=sections[session.section][0], instructions=sections[session.section][1]) # instructions page based on section
    else:
        session.export_data()
        sessions.remove_session(request.cookies.get('id'))
        app.logger.info(f"{session.student_id}: finished test and exported data. Cleaning up")
        return render_template('result.html')
        

@app.route('/continue_test', methods=['POST'])
def continue_test(): # redirect to correct page
    if not(has_session()): # redirects to home if session not found
        app.logger.warning(f"{request.cookies.get('id')}: No session detected, redirecting home")
        return redirect('/')
    
    session = get_session()
    match session.section:
        case 0 | 1:
            return redirect("/mcq-question")
        case 2 | 3 | 4:
            return redirect("/frq-question")

# this function will return question page
@app.route('/mcq-question', methods=['GET'])
def create_mcq_question_page():
    if not(has_session()): # redirects to home if session not found
        app.logger.warning(f"{request.cookies.get('id')}: No session detected, redirecting home")
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
        get_session().student_data.append(float(session.theta))
        get_session().export_data()
        return redirect('/instruction')
    
    prompt, questions, options = session.get_question() # get question data
    # set question counter (range if multiple questions)
    if len(questions) == 1: questionnumber = len(session.questions_answered)
    else: questionnumber = str(len(session.questions_answered) - len(questions) + 1) + " - " + str(len(session.questions_answered))
    match session.section:
        case 0: 
            app.logger.info(f"{get_session().student_id}: reading, prompt: {prompt}, questions: {questions}, question number: {questionnumber}")
            return render_template('reading.html', prompt=prompt, questions=questions, options=options, questionnumber=questionnumber)
        case 1:
            app.logger.info(f"{get_session().student_id}: listening, prompt: {prompt}, question number: {questionnumber}")
            return render_template('listening.html', audio=prompt, questions=questions, options=options, questionnumber=questionnumber)

# Route to handle form submission
@app.route('/submit_mcq', methods=['POST'])
def submit_mcq():
    if not(has_session()):
        app.logger.warning(f"{request.cookies.get('id')}: No session detected, redirecting home")
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
    app.logger.info(f"{get_session().student_id}: mcq answers checked, new theta: {session.theta}")
    get_session().student_data_adv[get_session().section].append(session.theta)
    return redirect('/mcq-question')

@app.route('/frq-question', methods=['GET'])
def create_frq_question_page():
    if not(has_session()): # redirects to home if session not found
        app.logger.warning(f"{request.cookies.get('id')}: No session detected, redirecting home")
        return redirect('/')
    
    session = get_session()
    match session.section:
        case 2:
            prompt, _ = session.free_response.select_prompt(session.section)
            app.logger.info(f"{session.student_id}: speaking, prompt: {prompt}")
            return render_template('speaking.html', prompt=prompt)
        case 3:
            prompt, session.writing_prompt = session.free_response.select_prompt(session.section)
            app.logger.info(f"{session.student_id}: writing1, prompt: {prompt}")
            return render_template('writing.html', prompt=prompt, textbox = True)        
        case 4:
            prompt, _ = session.free_response.select_prompt(session.section)
            app.logger.info(f"{session.student_id}: writing2, prompt: {prompt}")
            return render_template('writing.html', prompt=prompt, textbox = False)

@app.route('/upload-speaking', methods=['POST'])
def upload_speaking():
    if not(has_session()): # redirects to home if session not found
        app.logger.warning(f"{request.cookies.get('id')}: No session detected, redirecting home")
        return redirect('/')

    session = get_session()
    request.files['file'].save(f"data/student_data/{session.student_id}/speaking{splitext(request.files['file'].filename)[1]}")
    app.logger.info(f"{session.student_id}: speaking file saved")
    session.section += 1
    return redirect('/instruction')

@app.route('/submit-writing', methods=['POST'])
def submit_writing():
    if not(has_session()): # redirects to home if session not found
        app.logger.warning(f"{request.cookies.get('id')}: No session detected, redirecting home")
        return redirect('/')

    session = get_session()
    session.section += 1
    session.student_data.append(request.form.get('frq'))
    app.logger.info(f"{session.student_id}: writing saved")
    session.export_data()
    return redirect('/instruction')

def run():
    server = make_server("0.0.0.0", 3001, app)
    app.logger.info("Server startup")
    server.serve_forever()

if __name__ == '__main__':
    run()
    allow_connections = True