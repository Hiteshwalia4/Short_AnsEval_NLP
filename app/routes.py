from app import app, db, bcrypt
from flask import render_template, redirect, url_for, flash
from app.forms import RegisterForm, LoginForm,AnswerForm
from app.nlp import evaluate_answer
from app.models import User
from flask_login import login_user, login_required, logout_user

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
        user_to_create= User(username=form.username.data, email_address= form.email_address.data, password=hashed_password)

        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash( f"Account created succesfully. You are now logged in as { user_to_create.username }", category="sucess")

        return redirect(url_for("answers"))
    
    return render_template("register.html", form=form)


@app.route("/login", methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email_address=form.email_address.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password1):
            login_user(user)
            flash(f"Success!! You are logged in as: {user.username}", category='success')
            return redirect(url_for("answers"))
        else:
            flash("Incorrect User Name or Password!! Please Try Again.", category='danger')

    return render_template("login.html", form=form)        



@app.route("/answers", methods=['GET', 'POST'])
@login_required
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


@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out!!", category='info')
    return redirect(url_for("home"))
