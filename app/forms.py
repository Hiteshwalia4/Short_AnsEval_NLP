from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegisterForm(FlaskForm):
    username=StringField(label="User name", validators=[DataRequired(), Length(min=2,max=25)])
    email_address=StringField(label="E-mail Address", validators=[DataRequired(),Email()])
    password1= PasswordField(label="Password", validators=[DataRequired(), Length(min=6)])
    password2= PasswordField(label="Confirm Password", validators=[DataRequired(), EqualTo('password1')])
    submit=SubmitField(label="Create Account")
     
    def validate_username(self, username_to_check):
       user=User.query.filter_by(username=username_to_check.data).first()
       if user:
           raise ValidationError("Username already exists. Please try a different user.")
    
    def validate_email_address(self, email_to_check):
       email=User.query.filter_by(email_address=email_to_check.data).first()
       if email:
           raise ValidationError("Email Id already exists, try a different Email-Id.")
          

class LoginForm(FlaskForm):
    email=StringField(label="Email Address", validators=[DataRequired(),Email()])    
    password=PasswordField(label="Password", validators=[DataRequired()])   
    submit=SubmitField(label="Sign In") 


class AnswerForm(FlaskForm):
    answer1 = StringField(label="Answer 1:", validators=[DataRequired()])
    answer2 = StringField(label="Answer 2:", validators=[DataRequired()])
    answer3 = StringField(label="Answer 3:", validators=[DataRequired()])
    submit = SubmitField(label="Submit")
