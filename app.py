import psycopg2
from models import get_all_questions
from ui import display_menu, handle_menu


def main():
    while True:
        display_menu()
        handle_menu()


if __name__ == "__main__":
    main()
