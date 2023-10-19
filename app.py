import os
import requests

from flask import Flask, jsonify, session, request
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

FILE_URI = 'postgresql://postgres:12345@db:5432/questions'

app = Flask(__name__)

app.secret_key = "secret-string"
app.config['SQLALCHEMY_DATABASE_URI'] = FILE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(250), nullable=False)


def get_json(count: int):
    parameters = {
        "count": count,
    }
    response = requests.get(url="https://jservice.io/api/random", params=parameters)
    return response.json()

def import_unique_question(question):
    questions = []
    questions.append(question)
    data = get_json(1)
    if data[0]["question"] in questions:
        import_unique_question(question)
    else:
        new_id = data[0]["id"]
        new_question = data[0]["question"]
        new_answer = data[0]["answer"]
        new_date = data[0]["created_at"]

    return new_id, new_question, new_answer, new_date

def commit_to_db(id, question, answer, date):
    new_question = Question(
        id=id,
        question=question,
        answer=answer,
        date=date,
    )
    db.session.add(new_question)
    db.session.commit()

def get_previous_request(count: int):
    last_questions = Question.query.order_by(Question.id.desc()).limit(count).all()
    return last_questions


def fill_db(data):
    for element in range(len(data)):
        id = data[element]["id"]
        question = data[element]["question"]
        answer = data[element]["answer"]
        date = data[element]["created_at"]

        if Question.query.filter_by(question=question).first():
            new_id, new_question, new_answer, new_date = import_unique_question(question)
            commit_to_db(new_id, new_question, new_answer, new_date)
        else:
            commit_to_db(id, question, answer, date)

def get_questions(count):
    db.create_all()
    data = get_json(count)

    previous_count = session.get('previous_count')

    last_questions = get_previous_request(previous_count or count)
    session['previous_count'] = count

    if last_questions:
        response_data = []
        for question in last_questions:
            response_data.append({
                'id': question.id,
                'question': question.question,
                'answer': question.answer,
                'date': question.date,
            })
        fill_db(data)
        return jsonify(response_data)

    else:
        fill_db(data)
        return jsonify(response={'null': 'null'})

@app.route('/')
def welcome():
    return "<h1>Flask application is up and running!</h1>"

@app.route('/api/', methods=['POST'])
def process_post_request():

    data = request.json
    questions_num = data.get('questions_num')
    if questions_num:
        return get_questions(questions_num)
    else:
        return f'Incorrect request'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
