from app import db,app, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    username=db.Column(db.String(length=25), unique=True, nullable=False)
    email_address= db.Column(db.String(length=50), unique=True, nullable=False)
    password=db.Column(db.String(length=60), nullable=False)

    def __repr__(self):
        return f"User {self.username}"
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(30), nullable=False)
    ques = db.Column(db.Text, nullable=False)
    ans = db.Column(db.Text, nullable=False)

    
with app.app_context():
    db.create_all()
   
