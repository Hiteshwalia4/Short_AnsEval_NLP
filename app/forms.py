from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class AnswerForm(FlaskForm):
    answer1 = StringField(label="Answer 1:", validators=[DataRequired()])
    answer2 = StringField(label="Answer 2:", validators=[DataRequired()])
    answer3 = StringField(label="Answer 3:", validators=[DataRequired()])
    submit = SubmitField(label="Submit")