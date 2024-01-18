from db import connection_handler
from passlib.hash import bcrypt


@connection_handler
def register_user(cursor, username, password):
    hashed_password = bcrypt.hash(password)
    cursor.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id;",
        (username, hashed_password),
    )
    return cursor.fetchone()['id']


@connection_handler
def login_user(cursor, username, password):
    cursor.execute(
        "SELECT id, password FROM users WHERE username = %s;",
        (username,),
    )
    user_data = cursor.fetchone()
    if user_data and bcrypt.verify(password, user_data[1]):
        return user_data[0]
    return None


@connection_handler
def post_question(cursor, user_id, title, content):
    cursor.execute(
        "INSERT INTO questions (title, content, user_id) VALUES (%s, %s, %s) RETURNING id;",
        (title, content, user_id),
    )
    return cursor.fetchone()['id']


@connection_handler
def post_answer(cursor, user_id, question_id, content):
    cursor.execute(
        "INSERT INTO answers (content, user_id, question_id) VALUES (%s, %s, %s) RETURNING id;",
        (content, user_id, question_id),
    )
    return cursor.fetchone()['id']


@connection_handler
def edit_question(cursor, user_id, question_id, new_title, new_content):
    cursor.execute(
        "UPDATE questions SET title = %s, content = %s WHERE id = %s AND user_id = %s;",
        (new_title, new_content, question_id, user_id),
    )


@connection_handler
def edit_answer(cursor, user_id, answer_id, new_content):
    cursor.execute(
        "UPDATE answers SET content = %s WHERE id = %s AND user_id = %s;",
        (new_content, answer_id, user_id),
    )


@connection_handler
def delete_question(cursor, user_id, question_id):
    cursor.execute(
        "DELETE FROM questions WHERE id = %s AND user_id = %s;",
        (question_id, user_id),
    )


@connection_handler
def delete_answer(cursor, user_id, answer_id):
    cursor.execute(
        "DELETE FROM answers WHERE id = %s AND user_id = %s;",
        (answer_id, user_id),
    )


@connection_handler
def get_all_questions(cursor):
    cursor.execute(
        "SELECT id, title FROM questions ORDER BY created_at DESC;"
    )
    return cursor.fetchall()


@connection_handler
def get_question_with_answers(cursor, question_id):
    cursor.execute(
        "SELECT id, title, content FROM questions WHERE id = %s;",
        (question_id,),
    )
    question = cursor.fetchone()
    if question:
        cursor.execute(
            "SELECT id, content FROM answers WHERE question_id = %s ORDER BY created_at ASC;",
            (question_id,),
        )
        answers = cursor.fetchall()
        return question, answers
    return None, []


@connection_handler
def check_answer_author(cursor, user_id, answer_id):
    cursor.execute(
        "SELECT user_id FROM answers WHERE id = %s;",
        (answer_id,)
    )
    author_id = cursor.fetchone()

    return author_id == user_id if author_id else False


@connection_handler
def check_question_author(cursor, user_id, question_id):
    cursor.execute(
        "SELECT user_id FROM questions WHERE id = %s;",
        (question_id,)
    )
    author_id = cursor.fetchone()

    return author_id == user_id if author_id else False


@connection_handler
def order_and_filter_questions(cursor, criteria):
    criteria_mapping = {
        'date': 'created_at DESC',
        'author': 'user_id',
        'title': 'title',
    }

    valid_criteria = criteria_mapping.get(criteria)
    if not valid_criteria:
        raise ValueError("Invalid criteria. Supported criteria: date, author, title.")

    query = f"SELECT id, title FROM questions ORDER BY {valid_criteria};"
    cursor.execute(query)
    questions = cursor.fetchall()

    return questions


@connection_handler
def get_all_users(cursor):
    cursor.execute(
        "SELECT id, username FROM users;"
    )
    return cursor.fetchall()


@connection_handler
def get_all_answers(cursor, order_by='date'):
    valid_order_criteria = {
        'date': 'created_at DESC',
        'author': 'user_id',
    }
    if order_by not in valid_order_criteria:
        raise ValueError("Invalid order criteria. Supported criteria: date, user_id, question_id.")

    query = f"SELECT id, content, user_id, question_id, created_at FROM answers ORDER BY {valid_order_criteria[order_by]};"
    cursor.execute(query)
    return cursor.fetchall()


@connection_handler
def questions_with_more_than_x_answers(cursor, x):
    cursor.execute(
        "SELECT questions.id, title, COUNT(*) as answer_count FROM questions JOIN answers ON questions.id = answers.question_id GROUP BY questions.id HAVING COUNT(*) > %s;",
        (x,),
    )
    return cursor.fetchall()


@connection_handler
def answers_longer_than_x_characters(cursor, x):
    cursor.execute(
        "SELECT id, content, user_id, question_id FROM answers WHERE LENGTH(content) > %s;",
        (x,),
    )
    return cursor.fetchall()


@connection_handler
def get_user_info(cursor, user_id):
    cursor.execute(
        "SELECT id, username FROM users WHERE id = %s;",
        (user_id,),
    )
    user = cursor.fetchone()

    if user:
        cursor.execute(
            "SELECT id, title FROM questions WHERE user_id = %s;",
            (user_id,),
        )
        user['questions'] = cursor.fetchall()

        cursor.execute(
            "SELECT id, content FROM answers WHERE user_id = %s;",
            (user_id,),
        )
        user['answers'] = cursor.fetchall()

    return user


@connection_handler
def get_user_details(cursor, user_id):
    cursor.execute(
        "SELECT id, username FROM users WHERE id = %s;",
        (user_id,),
    )
    user = cursor.fetchone()

    if user:
        cursor.execute(
            "SELECT id, title FROM questions WHERE user_id = %s;",
            (user_id,),
        )
        user['questions'] = cursor.fetchall()

        cursor.execute(
            "SELECT id, content FROM answers WHERE user_id = %s;",
            (user_id,),
        )
        user['answers'] = cursor.fetchall()

    return user


@connection_handler
def get_answers_for_question(cursor, question_id):
    cursor.execute(
        "SELECT id, content, user_id FROM answers WHERE question_id = %s;",
        (question_id,),
    )
    return cursor.fetchall()
