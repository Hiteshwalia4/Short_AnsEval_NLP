from app import app
from flask import render_template, redirect, url_for
from app.forms import AnswerForm
from app.nlp import evaluate_answer

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/answers", methods=['GET', 'POST'])
def answers():
    form = AnswerForm()
    if form.validate_on_submit():
        reference_answer1 = "Python is an interpreted programming language that runs code line by line without earlier compiling the whole program into machine language."
        user_answer1 = form.answer1.data
        result1 = evaluate_answer(user_answer1, reference_answer1)

        reference_answer2 = "A decorator is a design pattern in Python that allows a user to add new functionality to an existing object without modifying its structure."
        user_answer2 = form.answer2.data
        result2 = evaluate_answer( user_answer2, reference_answer2)

        reference_answer3 = "A namespace is a way of providing the unique name for each object in Python."
        user_answer3 = form.answer3.data
        result3 = evaluate_answer(user_answer3, reference_answer3)

        return redirect(url_for("results", result1=result1, result2=result2, result3=result3))

    return render_template('answers.html', form=form)
