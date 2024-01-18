from models import (
    register_user as db_register_user,
    login_user as db_login_user,
    post_question as db_post_question,
    post_answer as db_post_answer,
    edit_question as db_edit_question,
    edit_answer as db_edit_answer,
    delete_question as db_delete_question,
    delete_answer as db_delete_answer,
    get_all_questions as db_get_all_questions,
    get_question_with_answers as db_get_question_with_answers,
    check_answer_author as db_check_answer_author,
    check_question_author as db_check_question_author,
    order_and_filter_questions as db_order_and_filter_questions
)
from datetime import datetime

logged_in_user = 1


def register_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    try:
        user_id = db_register_user(username, password)
        print(f"User registered successfully. Your user ID is: {user_id}")
    except Exception as e:
        print(f"Registration failed. Error: {e}")


def login_user():
    global logged_in_user
    if logged_in_user:
        print("You are already logged in.")
        return

    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user_id = db_login_user(username, password)
    if user_id is not None:
        logged_in_user = user_id
        print("Login successful.")
    else:
        print("Login failed. Invalid username or password.")


def post_question():
    global logged_in_user
    if logged_in_user is None:
        print("You need to log in to post a question.")
        return

    title = input("Enter the title of your question: ")
    content = input("Enter the content of your question: ")
    question_id = db_post_question(logged_in_user, title, content)
    print(f"Question posted successfully. Question ID: {question_id}")


def post_answer():
    global logged_in_user
    if logged_in_user is None:
        print("You need to log in to post an answer.")
        return

    question_id = int(input("Enter the question ID you want to answer: "))
    content = input("Enter the content of your answer: ")
    answer_id = db_post_answer(logged_in_user, question_id, content)
    print(f"Answer posted successfully. Answer ID: {answer_id}")


def edit_question():
    global logged_in_user
    if logged_in_user is None:
        print("You need to log in to edit a question.")
        return

    question_id = int(input("Enter the ID of the question you want to edit: "))

    if db_check_question_author(logged_in_user, question_id):
        new_title = input("Enter the new title for the question: ")
        new_content = input("Enter the new content for the question: ")
        db_edit_question(logged_in_user, question_id, new_title, new_content)
        print("Question edited successfully.")
    else:
        print("You are not the author of this question. Cannot edit.")


def edit_answer():
    global logged_in_user
    if logged_in_user is None:
        print("You need to log in to edit an answer.")
        return

    answer_id = int(input("Enter the ID of the answer you want to edit: "))

    if db_check_answer_author(logged_in_user, answer_id):
        new_content = input("Enter the new content for the answer: ")
        db_edit_answer(logged_in_user, answer_id, new_content)
        print("Answer edited successfully.")
    else:
        print("You are not the author of this answer. Cannot edit.")


def delete_question():
    global logged_in_user
    if logged_in_user is None:
        print("You need to log in to delete a question.")
        return

    question_id = int(input("Enter the ID of the question you want to delete: "))

    if db_check_question_author(logged_in_user, question_id):
        db_delete_question(logged_in_user, question_id)
        print("Question deleted successfully.")
    else:
        print("You are not the author of this question. Cannot delete.")


def delete_answer():
    global logged_in_user
    if logged_in_user is None:
        print("You need to log in to delete an answer.")
        return

    answer_id = int(input("Enter the ID of the answer you want to delete: "))

    if db_check_answer_author(logged_in_user, answer_id):
        db_delete_answer(logged_in_user, answer_id)
        print("Answer deleted successfully.")
    else:
        print("You are not the author of this answer. Cannot delete.")


def order_and_filter_questions():
    criteria = input("Enter the criteria for ordering and filtering (e.g., date, author, title): ")
    result = db_order_and_filter_questions(criteria)
    for question in result:
        print_question(question)


def get_question_with_answers_handler():
    user_idx = int(input("Enter your question id: "))
    print_question_and_answer(*db_get_question_with_answers(user_idx))


def get_all_questions_handler():
    for question in db_get_all_questions():
        print_question(question)


def exit_app():
    exit()


actions_dict = {
    1: {'title': 'View all questions', 'safe': True, 'action': get_all_questions_handler, 'args': ()},
    2: {'title': 'View specific question', 'safe': True, 'action': get_question_with_answers_handler, 'args': ()},
    3: {'title': 'Register', 'safe': False, 'action': register_user, 'args': ()},
    4: {'title': 'Log in', 'safe': False, 'action': login_user, 'args': ()},
    5: {'title': 'Log out', 'safe': True, 'action': print, 'args': ()},
    6: {'title': 'Post a question', 'safe': True, 'action': post_question, 'args': ()},
    7: {'title': 'Post an answer', 'safe': True, 'action': post_answer, 'args': ()},
    8: {'title': 'Edit a question', 'safe': True, 'action': edit_question, 'args': ()},
    9: {'title': 'Edit an answer', 'safe': True, 'action': edit_answer, 'args': ()},
    10: {'title': 'Delete a question', 'safe': True, 'action': delete_question, 'args': ()},
    11: {'title': 'Delete an answer', 'safe': True, 'action': delete_answer, 'args': ()},
    12: {'title': 'Order and filter questions', 'safe': False, 'action': order_and_filter_questions, 'args': ()},
    13: {'title': 'Exit', 'safe': False, 'action': exit_app, 'args': ()},
}


def display_menu():
    print('-'*30)
    for idx, row in actions_dict.items():
        if (logged_in_user is not None) == row['safe']:
            print(f'{idx}. {row['title']}')
    print('-'*30)


def handle_menu():
    user_choice = int(input("Enter your choice: "))
    if user_choice in actions_dict:
        action = actions_dict[user_choice]
        action['action']()


def print_question(question):
    print(f'{question['id']}. QUESTION: {question['title']}')


def print_question_and_answer(question, answers):
    print_question(question)
    for answer in answers:
        print(f'\t{answer['id']}. ANSWER: {answer['content']}')


display_menu()
handle_menu()
