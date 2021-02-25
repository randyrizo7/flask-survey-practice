from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def show_survey_start():
    """Start Survey """

    return render_template('start_survey.html', survey=survey)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session[RESPONSES_KEY] = []

    return redirect("/questions/0")

@app.route("/answer", methods=["POST"])
def handle_question():
    """zsave a response and redirect to next question"""

    #get the response choice 
    choice = request.form['answer']

    #add this to reponse session
    responses = session[RESPONSES_KEY]
    responses.append(choice)
    session[RESPONSES_KEY] = responses

    if (len(responses) == len(survey.questions)):
        # They've answered all the questions! Thank them.
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/questions/<int:qid>")
def show_question(qid):
    """show current question"""
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        #trying to access the question pages too soooon
        return redirect("/complete")

    if (len(responses) == len(survey.questions)):
        # If they answered all questions, thank them
        return redirect("/complete")
    
    if (len(responses) != qid):
        # Attempting to access questions out of order
        flash(f"invalid question id: {qid}")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template("questions.html", question=question)

@app.route("/complete")
def complete():
    """Survey complete. Show completion page."""

    return render_template("completion.html")