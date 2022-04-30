# Write your code here
import random
import json
from io import StringIO
import argparse


class Flashcards:
    def __init__(self, _import_from=None, _export_to=None):
        self.cards = {}
        self.term = ""
        self.definition = ""
        self.answer = ""
        self.file_name = ""
        self.error = 0
        self.logs = StringIO()
        self.import_from = _import_from
        self.export_to = _export_to

    def save_to_log(self):
        file_name = input("File name: \n")
        self.logs.seek(0)  # moving curser to 0
        text = self.logs.read()
        with open(file_name, mode="a", encoding="utf-8") as file:
            file.write(text)
        print("The log has been saved")

    def hardest_card(self):
        try:
            hardest_count = max([v["error"] for v in self.cards.values()])
        except:
            hardest_count = 0
        if hardest_count == 0:
            print("There are no cards with errors.")
            self.logs.write("There are no cards with errors.\n")

        else:
            cards = []
            for k, v in self.cards.items():
                if v["error"] == hardest_count:
                    cards.append(f'"{k}"')
            if len(cards) == 1:
                print(f'The hardest card is {cards[0]}. You have {hardest_count} errors answering it')
                self.logs.write(f'The hardest card is {cards[0]}. You have {hardest_count} errors answering it\n')
            else:
                cards = ", ".join(cards)
                print(f'The hardest cards are {cards}')
                self.logs.write(f'The hardest cards are {cards}\n')

    def reset_stats(self):
        for k, v in self.cards.items():
            v["error"] = 0
        print("Card statistics have been reset.")
        self.logs.write("Card statistics have been reset.\n")

    def export_cards(self):
        if not self.export_to:
            self.file_name = input("File name: \n")
            self.logs.write("File name: \n")
            self.logs.write(f"{self.file_name}\n")
        else:
            self.file_name = self.export_to
        with open(self.file_name, mode="w", encoding="utf-8") as file:
            json.dump(self.cards, file)
            print(f"{len(self.cards)} cards have been saved.")
            self.logs.write(f"{len(self.cards)} cards have been saved.\n")

    def import_cards(self):
        if not self.import_from:
            self.file_name = input("File name: \n")
            self.logs.write("File name: \n")
            self.logs.write(f"{self.file_name}\n")
        else:
            self.file_name = self.import_from
        try:
            with open(self.file_name, mode="r", encoding="utf-8") as file:
                cards = json.load(file)
                for k, v in cards.items():
                    self.cards.update({k: v})
                print(f"{len(cards)} cards have been loaded.")
                self.logs.write(f"{len(cards)} cards have been loaded.\n")
        except:
            print("File not found.")
            self.logs.write("File not found.\n")

    def remove_card(self):
        card = input("Which card? \n")
        self.logs.write("Which card? \n")
        self.logs.write(f"{card}\n")
        try:
            self.cards.pop(card)
            print("The card has been removed.")
            self.logs.write("The card has been removed.\n")
        except:
            print(f'Can\'t remove "{card}": there is no such card.')
            self.logs.write(f'Can\'t remove "{card}": there is no such card.\n')

    def add_card(self):
        self.term = input(f"The card: \n")
        self.logs.write(f"The card: \n")
        self.logs.write(f"{self.term}\n")
        while True:
            if self.term in self.cards.keys():
                print(f'The card "{self.term}" already exists. Try again:')
                self.logs.write('The card "{self.term}" already exists. Try again:\n')
                self.term = input()
                self.logs.write(f"{self.term}\n")
            else:
                break
        self.definition = input(f"The definition of the card: \n")
        self.logs.write(f"The definition of the card: \n")
        self.logs.write(f"{self.definition}\n")
        while True:
            if any([True if self.definition == v["definition"] else False for k, v in self.cards.items()]):
                print(f'The definition "{self.definition}" already exists. Try again:')
                self.logs.write(f'The definition "{self.definition}" already exists. Try again:\n')
                self.definition = input()
                self.logs.write(f"{self.definition}\n")
            else:
                print(f'The pair ("{self.term}":"{self.definition}") has been added.')
                self.logs.write(f'The pair ("{self.term}":"{self.definition}") has been added.\n')
                break
        self.cards.update({self.term: {"definition": self.definition, "error": 0}})

    def ask(self):
        try:
            count = int(input(f"How many times to ask? \n"))
            self.logs.write(f"How many times to ask? \n")
            self.logs.write(f"{count}\n")
        except:
            return
        for c in range(count):
            try:
                _term = random.choice(list(self.cards.keys()))
            except:
                return
            self.answer = input(f'Print the definition of "{_term}: \n')
            self.logs.write(f'Print the definition of "{_term}: \n')
            self.logs.write(f"{self.answer}\n")

            if self.cards[_term]["definition"] == self.answer:
                print("Correct!")
                self.logs.write("Correct!\n")
            elif any([True if self.answer == v["definition"] else False for k, v in self.cards.items()]):
                other_term = [k for k, v in self.cards.items() if self.answer == v["definition"]][0]
                print(
                    f'Wrong. The right answer is "{self.cards[_term]["definition"]}", but your definition is correct for "{other_term}".')
                self.logs.write(
                    f'Wrong. The right answer is "{self.cards[_term]["definition"]}", but your definition is correct for "{other_term}".\n')
                error = self.cards[_term]["error"]
                self.cards[_term]["error"] = error + 1
            else:
                print(f'Wrong. The right answer is "{self.cards[_term]["definition"]}".')
                self.logs.write(f'Wrong. The right answer is "{self.cards[_term]["definition"]}".\n')
                error = self.cards[_term]["error"]
                self.cards[_term]["error"] = error + 1

    def start(self):
        while True:
            if self.import_from:
                self.import_cards()
            print()
            action = input(
                "Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats): \n")
            self.logs.write(
                f"Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats): \n")
            self.logs.write(action + "\n")
            if action == "exit":
                if self.export_to:
                    self.export_cards()
                print("Bye bye!")
                self.logs.write("Bye bye!" + "\n")
                return
            elif action == "add":
                self.add_card()
            elif action == "remove":
                self.remove_card()
            elif action == "ask":
                self.ask()
            elif action == "export":
                self.export_cards()
            elif action == "import":
                self.import_cards()
            elif action == "reset stats":
                self.reset_stats()
            elif action == "hardest card":
                self.hardest_card()
            elif action == "log":
                self.save_to_log()


def main():
    parser = argparse.ArgumentParser(description="Flashcards")
    parser.add_argument("--import_from", help="file name to import")
    parser.add_argument("--export_to", help="file name to export")
    args = parser.parse_args()
    f = Flashcards(args.import_from, args.export_to)
    f.start()


if __name__ == "__main__":
    main()
