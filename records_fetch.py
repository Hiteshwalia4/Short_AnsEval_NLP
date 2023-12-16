from app.models import Question, User  
from app import app
def retrieve_records():
    with app.app_context():
    # Query all records from the Question table
        all_records = Question.query.all()
        all=User.query.all()

    # Print or process the retrieved records
        for record in all_records:
            print(f"Subject: {record.subject}, Question: {record.ques}, Answer: {record.ans}")
            print()
        for record in all:
            print(f"Username: {record.username}, E-mail: {record.email_address}")
            print()

# Call the function to retrieve and display records
retrieve_records()
