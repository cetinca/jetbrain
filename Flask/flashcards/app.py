from flashcard import Flashcard

main_menu_message = """
1. Add flashcards
2. Practice flashcards
3. Exit"""

add_card_message = """
1. Add a new flashcard
2. Exit"""

no_card_message = """
There is no flashcard to practice!"""

practice_card_message = """press "y" to see the answer:
press "n" to skip:
press "u" to update:"""

update_card_message = """press "d" to delete the flashcard:
press "e" to edit the flashcard:"""

check_answer_message = """press "y" if your answer is correct:
press "n" if your answer is wrong:"""


def main():
    while True:
        menu = {"1": add, "2": practice, "3": _exit, }
        print(main_menu_message)
        selection = input()
        try:
            result = menu[selection]()
            if not result:
                return
        except KeyError:
            print(f"\n{selection} is not an option")


def ask_input(message):
    while True:
        print(f"{message}")
        entered = input().strip()
        if entered: return entered


def add():
    while True:
        print(add_card_message)
        entered = input()
        if entered == "1":
            question = ask_input("Question: ")
            answer = ask_input("Answer: ")
            Flashcard.add_flashcard(question, answer)
        elif entered == "2":
            return 1
        else:
            print(f"\n{entered} is not an option")


def update(card):
    while True:
        print(update_card_message)
        entered = input()
        if entered == "d":
            Flashcard.delete_flashcard(card)
            return 1
        elif entered == "e":
            print(f"current question: {card.question}")
            question = ask_input("please write a new question:\n")
            print(f"current answer: {card.answer}")
            answer = ask_input("please write a new answer:\n")
            Flashcard.update_attr(card, question=question, answer=answer)
            return 1
        else:
            print(f"\n{entered} is not an option")


def check_answer(card):
    entered = ask_input(check_answer_message)
    if entered == "y":
        if card.box == 1:
            Flashcard.update_attr(card, box=2)
        elif card.box == 2:
            Flashcard.update_attr(card, box=3)
        elif card.box == 3:
            Flashcard.delete_flashcard(card)
    else:
        Flashcard.update_attr(card, box=1)


def practice():
    box_numbers = [1, 2, 3]
    cards = Flashcard.find_by_box(box_numbers)
    if not len(cards):
        print(no_card_message)
    for card in cards:
        print(f"Question: {card.question}")
        print(practice_card_message)
        entered = input()
        if entered == "y":
            print(f"Answer: {card.answer}")
            check_answer(card)
        elif entered == "u":
            update(card)
    return 1


def _exit():
    print("\nBye!")


if __name__ == "__main__":
    main()
