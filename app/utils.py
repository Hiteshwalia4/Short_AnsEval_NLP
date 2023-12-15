from app import db
from random import sample
from app.models import Question
from csv import DictReader

def add_questions_from_csv():
    if Question.query.first() is not None:
        # Database is not empty, no need to add questions
        return
    
    with open('app/Questions.csv', 'r', encoding='utf-8') as csv_file:
        csv_reader = DictReader(csv_file)
        questions = [Question(subject=row['Subject'], ques=row['Ques'], ans=row['Ans']) for row in csv_reader]

    db.session.add_all(questions)
    db.session.commit()

def get_random_question(subject, count=3):
    # Ensure questions are added to the database on app initialization
    add_questions_from_csv()
    all_questions = Question.query.filter_by(subject=subject).all()

    # Shuffle the questions to ensure randomness
    shuffled_questions = sample(all_questions, count)

    random_questions = [{'question': question.ques, 'answer': question.ans} for question in shuffled_questions]

    return random_questions
