from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)

app.config["SECRET_KEY"] = "1234567890"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def display_start():
    return render_template("survery_start.html", survey=satisfaction_survey)


@app.route("/start", methods={"POST"})
def survey_start():
    session["responses"] = []
    return redirect("/questions/0")


@app.route("/questions/<int:q_num>")
def display_question(q_num):
    responses = session["responses"]

    # if len(responses) == len(satisfaction_survey.questions):
    #     return redirect("/finished")

    if len(responses) != q_num:
        flash(f"Trying to access invalid question: {q_num}")
        return redirect(f"/questions/{len(responses)}")

    question = satisfaction_survey.questions[q_num]
    return render_template("question.html", q_num=q_num, q=question)


@app.route("/answer", methods=["POST"])
def handling_answer():
    responses = session["responses"]
    answer = request.form["answer"]
    responses.append(answer)
    session["responses"] = responses

    if len(responses) == len(satisfaction_survey.questions):
        return redirect("/finished")
    else:
        return redirect(f"questions/{len(responses)}")


@app.route("/finished")
def done():
    return render_template("thank_you.html")
