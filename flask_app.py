from flask import Flask, jsonify, request
from models import (
    get_answers_for_question,
    get_question_with_answers,
    order_and_filter_questions,
    get_all_users,
    get_all_answers,
    questions_with_more_than_x_answers,
    answers_longer_than_x_characters,
    get_user_details,
)

app = Flask(__name__)


@app.route('/questions', methods=['GET'])
@app.route('/questions/<filter>', methods=['GET'])
def list_questions(filter='date'):
    try:
        questions = order_and_filter_questions(filter)
        return jsonify(questions)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/answers', methods=['GET'])
@app.route('/answers/<filter>', methods=['GET'])
def list_answers(filter='date'):
    try:
        answers = get_all_answers(filter)
        return jsonify(answers)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400


@app.route('/users', methods=['GET'])
def list_users():
    users = get_all_users()
    return jsonify(users)


@app.route('/question/<int:question_id>', methods=['GET'])
def get_question_by_id(question_id):
    question, answers = get_question_with_answers(question_id)
    if question:
        return jsonify({'question': question, 'answers': answers})
    else:
        return jsonify({'error': 'Question not found'}), 404


@app.route('/question/<int:question_id>/answers', methods=['GET'])
def list_answers_for_question(question_id):
    answers = get_answers_for_question(question_id)
    return jsonify(answers)


@app.route('/questions/more_than/<int:x>_answers', methods=['GET'])
def list_questions_more_than_x_answers(x):
    questions = questions_with_more_than_x_answers(x)
    return jsonify(questions)


@app.route('/answers/longer_than/<int:x>_characters', methods=['GET'])
def list_long_answers(x):
    answers = answers_longer_than_x_characters(x)
    return jsonify(answers)


@app.route('/users/<int:x>/details', methods=['GET'])
def list_user_details(x):
    users = get_user_details(x)
    return jsonify(users)


if __name__ == '__main__':
    app.run(debug=True)
