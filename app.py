# app.py
import psycopg2
from db import DATABASE_URL


def main():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    while True:
        print("\n1. View all questions")
        print("2. View a specific question and its answers")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            cursor.execute("SELECT * FROM questions;")
            questions = cursor.fetchall()
            display_questions_with_answers(questions)

        elif choice == "2":
            question_id = int(input("Enter the question ID: "))
            cursor.execute("SELECT * FROM questions WHERE id = %(question_id)s;", ({'question_id': question_id}))
            question = cursor.fetchone()
            cursor.execute("SELECT * FROM answers WHERE id = %(question_id)s;", ({'question_id': question_id}))
            answers = cursor.fetchall()
            if question:
                display_question_with_answers(question, answers)
            else:
                print("Question  not found.")
        elif choice == "3":
            break

    cursor.close()
    conn.close()


def display_questions_with_answers(questions):
    for question in questions:
        print(f"Question {question[0]}: {question[1]}")


def display_question_with_answers(question, answers):
    print(f"Question {question[0]}: {question[1]}")
    for answer in answers:
        print(f"\tAnswer {answer[0]}: {answer[1]}")


if __name__ == "__main__":
    main()
