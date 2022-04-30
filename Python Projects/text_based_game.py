# write your code here
import json
import sys
import os


class Game:
    messages = {
        "welcome": "***Welcome to the Journey to Mount Qaf***\n\n1- Press key '1' or type 'start' to "
                   "start a new game\n2- Press key '2' or type 'load' to load your progress\n3- Press key '3' "
                   "or type 'quit' to quit the game\n",
        "game_over": "The darkness said, \"Wrong!\" You try to run but it catches your legs and drags you to the "
                     "darkness...\nYou died! Lives remaining:  0\nYou've run out of lives! Game over!\n",
        "help": "Type the number of the option you want to choose.\nCommands you can use:\n/i => Shows "
                "inventory.\n/q => Exits the game.\n/c => Shows the character traits.\n/h => Shows help.\n",
        "quit": "Goodbye!",
        "difficulty": "Choose your difficulty:\n1- Easy\n2- Medium\n3- Hard\n",
        "no_data": "No save data found!",
        "going_back": "Going back to menu...",
    }

    def __init__(self):
        self.entered = ""
        self.user_name = ""
        self.char_name = ""
        self.char_species = ""
        self.char_gender = ""
        self.char_snack = ""
        self.char_weapon = ""
        self.char_tool = ""
        self.difficulty = ""
        self.char_lvl = 0
        self.scene_number = 0
        self.lives = 0
        self.inventory = []
        self.stack = []
        self.char_dict = {"char_attrs": {"name": "", "species": "", "gender": ""},
                          "inventory": {"snack": "", "weapon": "", "tool": ""}, "difficulty": "", "lives": 0,
                          "level": 0}
        self.menu = {"main": self.main_menu, "new_game": self.new_game, "info": self.char_info}
        self.diff_list = ["1", "2", "3", "easy", "medium", "hard"]
        self.commands = {
            "/h": self.show_help,
            "/i": self.show_inventory,
            "/q": self.quit_game,
            "/c": self.char_traits
        }

    @staticmethod
    def get_input(msg, values):
        while True:
            _entered = input().lower()
            if _entered in values:
                return _entered
            else:
                print(msg)

    @staticmethod
    def read_file(_name):
        with open(f"./game/saves/{_name}", "r") as file:
            content = json.load(file)
            return content

    @staticmethod
    def write_file(_content, _name):
        with open(f"./game/saves/{_name}.json", "w") as file:
            j = json.dumps(_content)
            file.write(j)

    def reset_params(self):
        self.char_lvl = 2
        self.scene_number = 1
        self.inventory = []
        self.stack = []
        if self.difficulty == "1" or self.difficulty == "easy":
            self.lives = 5
            self.difficulty = "Easy"
        elif self.difficulty == "2" or self.difficulty == "medium":
            self.lives = 3
            self.difficulty = "Medium"
        elif self.difficulty == "3" or self.difficulty == "hard":
            self.lives = 1
            self.difficulty = "Hard"

    def set_params(self, _user_name):
        self.user_name = _user_name
        self.char_name = self.char_dict["char_attrs"]["name"]
        self.char_species = self.char_dict["char_attrs"]["species"]
        self.char_gender = self.char_dict["char_attrs"]["gender"]
        self.char_snack = self.char_dict["inventory"]["snack"]
        self.char_weapon = self.char_dict["inventory"]["weapon"]
        self.char_tool = self.char_dict["inventory"]["tool"]
        self.difficulty = self.char_dict["difficulty"]
        self.lives = self.char_dict["lives"]
        self.char_lvl = self.char_dict["level"]
        self.scene_number = 1
        self.inventory = []
        self.stack = []

    def update_char_dict(self):
        self.char_dict.update(
            {"char_attrs": {"name": self.char_name, "species": self.char_species, "gender": self.char_gender},
             "inventory": {"snack": self.char_snack, "weapon": self.char_weapon, "tool": self.char_tool},
             "difficulty": self.difficulty, "lives": self.lives,
             "level": self.char_lvl})

    def quit_game(self):
        print("You sure you want to quit the game? Y/N")
        if input().lower() == "y":
            print(self.messages["quit"])
            self.update_char_dict()
            self.write_file(self.char_dict, self.user_name)
            sys.exit()
        else:
            return

    def exit_game(self):
        print(self.messages["quit"])
        self.update_char_dict()
        self.write_file(self.char_dict, self.user_name)
        sys.exit()

    def show_inventory(self):
        print(
            f"Your inventory: {self.char_snack.capitalize()}, {self.char_weapon.capitalize()}, "
            f"{self.char_tool.capitalize()}"
        )
        return

    def show_help(self):
        print(self.messages["help"])
        return

    def char_info(self):
        print(
            f"Your character: {self.char_name.capitalize()}, {self.char_species.capitalize()}, "
            f"{self.char_gender.capitalize()}"
        )
        print(
            f"Your inventory: {self.char_snack.capitalize()}, {self.char_weapon.capitalize()}, "
            f"{self.char_tool.capitalize()}"
        )
        print(f"Difficulty: {self.difficulty}")
        print(f"Lives: {self.lives}")

    def char_traits(self):
        print(
            f"Your character: {self.char_name.capitalize()}, {self.char_species.capitalize()}, "
            f"{self.char_gender.capitalize()}."
        )
        print(f"Lives remaining: {self.lives}")

    def go_back(self):
        if len(self.stack):
            print(self.messages["going_back"])
            return self.main_menu()
        else:
            print(self.messages["going_back"])
            return self.main_menu()

    def add_item(self, _item):
        self.inventory.append(_item)
        print(f"A new item has been added to your inventory: {_item}")
        return

    def remove_item(self, _item):
        self.inventory.remove(_item)
        print(f"An item has been removed from your inventory: {_item}")
        return

    def add_life(self):
        self.lives += 1
        print(f"You gained an extra lives! Lives remaining: {self.lives}")

    def remove_life(self):
        self.lives -= 1
        print(f"You died! Lives remaining: {self.lives}")
        print(f"Level {self.char_lvl}")
        if self.lives == 0:
            return
        return True

    @staticmethod
    def find_files():
        temp = []
        for root, dirs, files in os.walk("./game/saves", topdown=False):
            for name in files:
                if "." in name:
                    name, ext = name.split(".")
                    temp.append(name)
                else:
                    temp.append(name)
        return temp

    def check_options(self, _out):
        if "inventory-" in _out:
            first_index, second_index = _out.find("'"), _out.rfind("'")
            self.remove_item(_out[first_index + 1: second_index])
        if "inventory+" in _out:
            first_index, second_index = _out.find("'"), _out.rfind("'")
            self.add_item(_out[first_index + 1: second_index])
        if "move" in _out:
            self.scene_number += 1
        if "repeat" in _out:
            index = _out.find("(")
            print(_out[:index])
        if "life-1" in _out:
            result = self.remove_life()
            if not result:
                return
        if "life+1" in _out:
            self.add_life()
        self.update_char_dict()
        self.write_file(self.char_dict, self.user_name)
        return True

    def main_menu(self):
        print(self.messages["welcome"])
        self.stack.append("main")
        entered = input()
        if entered == "1" or entered.lower() == "start":
            print("Starting a new game...")
            return self.new_game()
        elif entered == "2" or entered.lower() == "load":
            temp = self.find_files()
            if temp:
                for t in temp:
                    print(t)
                print("Type your user name from the list:")
                user_name = input()
                try:
                    self.char_dict = self.read_file(f"{user_name}.json")

                except:
                    print(self.messages["no_data"])
                    return True
                else:
                    self.set_params(user_name)
                    return self.in_game()
            else:
                print(self.messages["no_data"])
                return True
        elif entered == "3" or entered.lower() == "quit":
            self.exit_game()
        else:
            print("Unknown input! Please enter a valid one.")
            return True

    def new_game(self):
        print("Enter a user name to save your progress or type '/b' to go back")
        entered = input()
        if entered == "/b":
            return self.go_back()
        else:
            self.user_name = entered
            print("Create your character:")
            print("1- Name")
            self.char_name = input()
            print("2- Species")
            self.char_species = input()
            print("3- Gender")
            self.char_gender = input()
            print("Pack your bag for the journey:")
            print("1- Favourite Snack")
            self.char_snack = input()
            print("2- A weapon for the journey")
            self.char_weapon = input()
            self.add_item(self.char_weapon)
            print("3- A traversal tool")
            self.char_tool = input()
            print(self.messages["difficulty"])
            self.difficulty = self.get_input(
                "Unknown input! Please enter a valid one.", ["1", "2", "3", "easy",
                                                             "medium", "hard"]
            )
            print("Good luck on your journey!")
            self.reset_params()
            self.update_char_dict()
            self.char_info()
        self.stack.append("new_game")
        return self.in_game()

    def in_game(self):
        # story = self.read_file("C:/Users/cetin/PycharmProjects/Text Based Adventure Game/Text Based Adventure Game/task/game/saves/story.json")
        story = self.read_file("story.json")
        print(f"Level {self.char_lvl}")
        while True:
            if self.scene_number == 4:
                self.char_lvl += 1
                self.scene_number = 1
                print(f"Level {self.char_lvl}")
                self.update_char_dict()
                self.write_file(self.char_dict, self.user_name)
            if self.char_lvl == 3:
                print(f"Congratulations! You beat the game!")
                return self.exit_game()
            print("\n" + story["story"][f"lvl{self.char_lvl}"]["scenes"][f"scene{self.scene_number}"] + "\n")
            print("What will you do? Type the number of the option or type '/h' to show help." + "\n")
            selection = []
            for k, v in story["choices"][f"lvl{self.char_lvl}"][f"scene{self.scene_number}"].items():
                print(f"{k[-1]}- {v}")
                selection.append(k[-1])
            entered = input()
            if entered in self.commands:
                self.commands[entered]()
            elif entered in selection:
                out = story["outcomes"][f"lvl{self.char_lvl}"][f"scene{self.scene_number}"][f"outcome{entered}"]
                if type(out) == str:
                    result = self.check_options(out)
                    if not result:
                        return True
                else:
                    for k, v in out.items():
                        if "inventory-" in v:
                            first_index, second_index = v.find("'"), v.rfind("'")
                            item = v[first_index + 1: second_index]
                            if item in self.inventory:
                                out = v
                            break
                        else:
                            out = v
                    result = self.check_options(out)
                    if not result:
                        return True
            else:
                print("Unknown input! Please enter a valid one")


def main():
    n = Game()
    n.write_file(n.messages, "messages")
    while True:
        response = n.main_menu()
        n.update_char_dict()
        n.write_file(n.char_dict, n.user_name)
        if not response: break


if __name__ == "__main__":
    main()
