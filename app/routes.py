from app import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request, session
from app.forms import RegisterForm, LoginForm,AnswerForm
from app.nlp import evaluate_answer
from app.models import User
from flask_login import login_user, login_required, logout_user
from app.utils import get_random_question

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
        flash( f"Account created succesfully. You are now logged in as { user_to_create.username }", category="success")

        return redirect(url_for("answers"))
    
    return render_template("register.html", form=form)


@app.route("/login", methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email_address=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash(f"Success!! You are logged in as: {user.username}", category='success')
            return redirect(url_for("answers"))
        else:
            flash("Incorrect User Name or Password!! Please Try Again.", category='danger')

    return render_template("login.html", form=form)        


# @app.route("/noofques", methods=['GET','POST'])
# def noofques():
#     form= AskNoOfQues()
#     py_count=form.python_count.data
#     jv_count=form.java_count.data
#     return redirect(url_for("answers"))

@app.route("/answers", methods=['GET', 'POST'])
@login_required
def answers():
    form = AnswerForm()
    # form2=AskNoOfQues()
    if form.validate_on_submit():
        # Form has been submitted with answers, retrieve questions from the session
        random_questions = session.get('random_questions')
        if not random_questions or 'Python' not in random_questions or 'Java' not in random_questions:
            # Session data is missing, redirect to avoid errors
            return redirect(url_for('answers'))

        python_questions = random_questions['Python']
        java_questions = random_questions['Java']

        python_reference_answers = [question['answer'] for question in python_questions]
        java_reference_answers = [question['answer'] for question in java_questions]
        
        # Separate user answers for Python and Java
        python_user_answers = [form[f'python_answer{i}'].data for i in range(1, len(python_questions)+1)]
        java_user_answers = [form[f'java_answer{i}'].data for i in range(1, len(java_questions)+1)]

        # Evaluate answers
        python_results = [evaluate_answer(user_ans, ref_ans) for user_ans, ref_ans in zip(python_user_answers, python_reference_answers)]
        java_results = [evaluate_answer(user_ans, ref_ans) for user_ans, ref_ans in zip(java_user_answers, java_reference_answers)]

        return redirect(url_for("results", 
                                python_results=python_results, java_results=java_results))

    # Form is being loaded for the first time, get random questions and store in session
    python_questions = get_random_question('Python')
    java_questions = get_random_question('Java')
    session['random_questions'] = {
            'Python': python_questions,
            'Java': java_questions
    }
    
    return render_template('answers.html', form=form, python_questions=session['random_questions']['Python'], java_questions=session['random_questions']['Java'])


@app.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out!!", category='info')
    return redirect(url_for("home"))


@app.route("/results", methods=['GET', 'POST'])
def results():
    python_results = request.args.getlist('python_results')
    java_results = request.args.getlist('java_results')
    python_questions=session['random_questions']['Python']
    java_questions=session['random_questions']['Java']
    return render_template("results.html", python_questions=python_questions, java_questions=java_questions,
                           python_results=python_results, java_results=java_results)

      