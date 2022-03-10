from flask import Flask, request, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

#memory of responses
response = []

RESPONSES_KEY = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

#get request to the home route
@app.route("/")
def show_intro():
    """show title of survey, instructions, and start button """
    return render_template("intro.html", survey=survey)

#survey button directs to /questions route
@app.route("/questions", methods=["POST"])
def start_survey():
    """to start, clear responses during the session"""
    session[RESPONSES_KEY] = []
    #directs to questions
    return redirect("/questions/0")


@app.route("/questions/<int:id>")
def show_question(id):
    """show survey questions base on id"""

    responses = session.get(RESPONSES_KEY)
    
    #accessing questions on page too soon
    if (response is None):
        return redirect("/")

    #equal in len = user has answered all questions
    if(len(responses) == len(survey.questions)):
        #redirects to completion page & thank them
        return redirect("/complete")

    #trying to access questions out of order.
    if (len(responses) != id):
        flash(f"Invalid question id: {id}.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[id]
    return render_template("questions.html", id=id, question=question)


@app.route("/answer", methods=["POST"])
def next_question():
    """redirects to next question"""

    #get answer
    ans = request.form['answer']

    # add this response to the session
    responses = session[RESPONSES_KEY]
    responses.append(ans)
    session[RESPONSES_KEY] = responses

    #answered all questions
    if(len(responses) == len(survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/complete")
def complete():
    """Survey complete & Show completion page."""

    return render_template("completion.html")