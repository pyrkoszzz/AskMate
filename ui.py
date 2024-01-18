from models import get_all_questions, get_question_with_answers




def exit_app():
    exit()


actions_dict = {
    1: {'title': 'View all questions', 'safe': False, 'action': get_all_questions, 'args': ()},
    2: {'title': 'View specific question', 'safe': False, 'action': get_question_with_answers, 'args': ()},
    3: {'title': 'Exit', 'safe': False, 'action': exit_app, 'args': ()},
}


def display_menu():
    for idx, row in actions_dict.items():
        print(f'{idx}. {row['title']}')


def handle_menu():
    user_choice = int(input("Enter your choice: "))
    if user_choice in actions_dict:
        action = actions_dict[user_choice]
        print(action['action'])


display_menu()
handle_menu()
