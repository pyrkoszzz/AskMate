from db import connection_handler


@connection_handler
def get_all_questions(cursor):
    cursor.execute("SELECT * FROM questions;")
    questions = cursor.fetchall()
    return questions


@connection_handler
def get_question_with_answers(cursor, idx):
    cursor.execute("SELECT * FROM questions WHERE id == %(idx)s", ({'idx': idx}))
    question = cursor.fetchone()
    cursor.execute("SELECT * FROM answers WHERE question_id == %(idx)s", ({'idx': idx}))
    answers = cursor.fetchall()
    return question, answers

