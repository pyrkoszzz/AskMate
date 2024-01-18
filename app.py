import psycopg2
from models import get_all_questions
from ui import display_menu, handle_menu


def main():
    while True:
        display_menu()
        handle_menu()


def display_questions_with_answers(questions):
    for question in questions:
        print(f"Question {question[0]}: {question[1]}")


def display_question_with_answers(question, answers):
    print(f"Question {question[0]}: {question[1]}")
    for answer in answers:
        print(f"\tAnswer {answer[0]}: {answer[1]}")


if __name__ == "__main__":
    main()
