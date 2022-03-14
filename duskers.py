import datetime
import json
import time
from adds import *
import argparse
from random import Random
import os
import re
import keyboard

greeting = "Greetings, commander {name}!"
begin = "Are you ready to begin?"
nothing_more = r"""Nothing more in sight.
       [Back]"""


class Game:
    def __init__(self, _seed, _min_sleep, _max_sleep, _names):
        self.name = ""
        self.command = ""
        self.short_sleep = 0.0001
        self.min_sleep = _min_sleep
        self.max_sleep = _max_sleep
        self.names = _names.replace(",", " ").split("/")
        self.titanium_found = 0
        self.game_seed = Random()
        self.animation_seed = Random()
        self.robots = 3
        self.game_seed.seed(_seed)
        self.animation_seed.seed(time.time())
        self.titanium_scanner = False
        self.encounter_scanner = False
        self.slot = 0
        self.last_save = ""

    @staticmethod
    def log_to_file(_text):
        with open(file="./log.txt", mode="a", encoding="utf-8") as file:
            file.write(f"{_text}\n")

    @staticmethod
    def create_test_values(_name="cetin", _score=1500, _robots=1, _titanium_scanner=True, _encounter_scanner=True,
                           _date="2021-10-29 16:58"):
        if not os.path.isfile("./save_file.txt"):
            content = {}
            content.update(
                {1: {"name": _name, "titanium": _score, "robots": _robots, "titanium_scanner": _titanium_scanner,
                     "encounter_scanner": _encounter_scanner, "last_save": _date}})
            text = json.dumps(content)
            with open(file="./save_file.txt", mode="w", encoding="utf-8") as file:
                file.write(text)
        # if not os.path.isfile("./high_scores.txt"):
        #     content = ([{"name": "cetin", "score": 1500}])
        #     text = json.dumps(content)
        #     with open(file="./high_scores.txt", mode="w", encoding="utf-8") as file:
        #         file.write(text)

    def save_scores(self):
        if os.path.isfile("./high_scores.txt"):
            with open(file="./high_scores.txt", mode="r", encoding="utf-8") as file:
                try:
                    content = file.read()
                    content = json.loads(content)
                except:
                    content = []
        else:
            content = []

        content.append({"name": self.name, "score": self.titanium_found})
        content = sorted(content, key=lambda x: int(x["score"]), reverse=True)
        content.pop() if len(content) > 10 else None

        with open(file="./high_scores.txt", mode="w", encoding="utf-8") as file:
            file.write(json.dumps(content))
        return

    def high(self):
        if os.path.isfile("./high_scores.txt"):
            with open(file="./high_scores.txt", mode="r", encoding="utf-8") as file:
                try:
                    content = json.loads(file.read())
                except:
                    content = []
                else:
                    print()
                    print("    HIGH SCORES")
                    print()
                    for i in range(10):
                        try:
                            c = content[i]
                            print(f'({i + 1}) {c["name"]} {c["score"]}')
                        except:
                            print(f"({i + 1})")
                            pass
                    print()
                    print("    [Back]")
                    print()
                    print("Your command:")
                    self.command = input()
                    if self.command.lower() == "back":
                        return
                    else:
                        return "exit"
        else:
            print()
            print("    HIGH SCORES")
            print()
            for i in range(10):
                print(f'({i + 1}) empty 0')

            print()
            print("    [Back]")
            print()
            print("Your command:")
            self.command = input()
            if self.command.lower() == "back":
                return
            else:
                return "exit"

    @staticmethod
    def help_me():
        print("""
        This is a fun game developed by TrueApp Co.
        Year 2021.
              """)
        print("Press enter key to continue")
        input()
        return

    def get_name(self):
        print()
        print("Enter your name:", end="")
        self.name = input()

    def animated_print(self, text, _interval):
        if self.min_sleep == 0 and self.max_sleep == 0:
            print(text)
        else:
            for t in text:
                print(t, end="")
                time.sleep(_interval)

    @staticmethod
    def read_file_content():
        if os.path.isfile("./save_file.txt"):
            with open(file="./save_file.txt", mode="r", encoding="utf-8") as file:
                return file.read()
        else:
            return

    def show_slots(self):
        content = self.read_file_content()
        s = content.split()
        name = s[0]
        titanium_found = int(s[2])
        robots = int(s[4])
        last_save = s[7] + " " + s[8]

        for i in ["1", "2", "3"]:
            if i == "1":
                print(
                    f'[{i}] {name} Titanium: {titanium_found} Robots: {robots} Last save: {last_save}')
            else:
                print(f"[{i}] empty")
            print()

    def load(self):
        while True:
            print("Select save slot:")
            self.show_slots()
            print()
            print("Your command:")
            self.slot = input()
            if self.slot == "back":
                return
            elif self.slot == "1":
                content = self.read_file_content()
                # self.log_to_file(f"load_{content}")
                s = content.split()
                if bool(re.match(r".*Titanium scanner", content)):
                    index = re.search(r".*Titanium scanner: ", content).end()
                    self.titanium_scanner = True if content[index:index + 4].lower() == "true" else False
                else:
                    self.titanium_scanner = False
                if bool(re.match(r".*Encounter scanner", content)):
                    index = re.search(r".*Encounter scanner: ", content).end()
                    self.encounter_scanner = True if content[index:index + 4].lower() == "true" else False
                else:
                    self.encounter_scanner = False
                self.name = s[0]
                self.titanium_found = int(s[2])
                self.robots = int(s[4])
                self.last_save = s[7] + " " + s[8]
                print(game_loaded)
                print(f"Welcome back, commander {self.name}")
                return self.game()
            else:
                print("Empty slot!")
                return

    def save_main(self):
        now = datetime.datetime.now()
        date_time = f"{now.year}-{now.month:02d}-{now.day:02d} {now.hour:02d}:{now.minute:02d}"
        text = f'{self.name} Titanium: {self.titanium_found} Robots: {self.robots} Last save: {date_time} Titanium scanner: {self.titanium_scanner} Encounter scanner: {self.encounter_scanner}'
        # self.log_to_file(f"save_main_{text}")
        with open(file="./save_file.txt", mode="w", encoding="utf-8") as file:
            file.write(text)
            print(game_saved)
        return "main"

    def save_exit(self):
        now = datetime.datetime.now()
        date_time = f"{now.year}-{now.month:02d}-{now.day:02d} {now.hour:02d}:{now.minute:02d}"
        text = f'{self.name} Titanium: {self.titanium_found} Robots: {self.robots} Last save: {date_time} Titanium scanner: {self.titanium_scanner} Encounter scanner: {self.encounter_scanner}'
        # self.log_to_file(f"save_exit_{text}")
        with open(file="./save_file.txt", mode="w", encoding="utf-8") as file:
            file.write(text)
            print(game_saved)
        return "exit"

    # def save(self):
    #     print("Select save slot:")
    #     content = self.read_file_content()
    #     content = json.loads(content)
    #     self.show_slots()
    #     slot = int(input())
    #     now = datetime.datetime.now()
    #     date_time = f"{now.year}-{now.month:02d}-{now.day:02d} {now.hour:02d}:{now.minute:02d}"
    #     content.update(
    #         {slot: {"name": self.name, "titanium": self.titanium_found, "robots": self.robots, "last_save": date_time,
    #                 "titanium_scanner": self.titanium_scanner, "encounter_scanner": self.encounter_scanner}})
    #     text = json.dumps(content)
    #     self.log_to_file(f"save_{text}")
    #     with open(file="./save_file.txt", mode="w", encoding="utf-8") as file:
    #         file.write(text)
    #         print(game_saved)
    #     return

    def save(self):
        print("Select save slot:")
        self.show_slots()
        slot = int(input())
        now = datetime.datetime.now()
        date_time = f"{now.year}-{now.month:02d}-{now.day:02d} {now.hour:02d}:{now.minute:02d}"
        text = f'{self.name} Titanium: {self.titanium_found} Robots: {self.robots} Last save: {date_time} Titanium scanner: {self.titanium_scanner} Encounter scanner: {self.encounter_scanner}'
        # self.log_to_file(f"save_{text}")
        with open(file="./save_file.txt", mode="w", encoding="utf-8") as file:
            file.write(text)
            print(game_saved)
        return

    def upgrade(self):
        print(upgrade_shop)
        while True:
            print("Your command: ", end="")
            self.command = input()
            if self.command.lower() == "back":
                return
            elif self.command == "1" and self.titanium_found > 250:
                self.titanium_scanner = True
                self.titanium_found -= 250
                print("Purchase successful. You can now see how much titanium you can get from each found location.")
                return
            elif self.command == "2" and self.titanium_found > 500:
                self.encounter_scanner = True
                self.titanium_found -= 500
                print(
                    "Purchase successful. You will now see how likely you will encounter an enemy at each found location.")
                return
            elif self.command == "3" and self.titanium_found > 1000:
                print("Purchase successful. You now have an additional robot")
                self.robots += 1
                self.titanium_found -= 1000
                return
            else:
                print("Not enough titanium!")

    def explore(self):
        index = 0
        names_found = {}
        titanium_per_zone = {}
        encounter_rate = {}
        self.command = "s"
        number = self.game_seed.randint(1, 9)  # max amount of zone to be discovered.
        while True:
            if self.command.isdigit():
                break
            if self.command.lower() == "back":
                return
            elif number == index:
                print(nothing_more)
            elif self.command.lower() == "s":
                index += 1
                # state = random.getstate()
                name = self.game_seed.choice(self.names)
                names_found.update({index: name})
                # random.setstate(state)
                titanium_per_zone.update({index: self.game_seed.randint(10, 100)})
                encounter_rate.update({index: self.game_seed.random()})
                print("Searching", end="")
                interval = int(self.animation_seed.randint(self.min_sleep, self.max_sleep))
                self.animated_print(interval * "." + "\n", 1)

                for k, v in names_found.items():
                    if self.titanium_scanner and self.encounter_scanner:
                        print(
                            f"[{k}] {v} Titanium: {titanium_per_zone[k]} Encounter rate: {round(encounter_rate[k] * 100, 0):.0f}%")
                    elif self.titanium_scanner:
                        print(f"[{k}] {v} Titanium: {titanium_per_zone[k]}")
                    elif self.encounter_scanner:
                        print(f"[{k}] {v} Encounter rate: {round(encounter_rate[k] * 100, 0):.0f}%")
                    else:
                        print(f"[{k}] {v}")
                print()
                print("[S] to continue searching")

            print()
            print("Your command:", end="")
            self.command = input()

        try:
            names_found[int(self.command)]
        except:
            return
        else:
            print("Deploying robots", end="")
            fight = self.game_seed.random()
            if fight < encounter_rate[int(self.command)]:
                print()
                print("Enemy encounter!!!")
                self.robots -= 1
                if self.robots != 0:
                    print(f"{names_found[int(self.command)]} explored successfully, 1 robot lost..")
                    self.titanium_found += titanium_per_zone[int(self.command)]
                    print(f"Acquired {titanium_per_zone[int(self.command)]} lumps of titanium")
                elif self.robots == 0:
                    print("Mission aborted, the last robot lost...")
                    self.log_to_file(f"{self.name} {self.titanium_found}")
                    print(game_over)
                    self.save_scores()
                    return self.save_main()
            else:
                interval = int(self.animation_seed.randint(self.min_sleep, self.max_sleep))
                self.animated_print(interval * ".", 1)
                print(f"{names_found[int(self.command)]} was explored successfully, with no damage taken.")
                self.titanium_found += titanium_per_zone[int(self.command)]
                print(f"Acquired {titanium_per_zone[int(self.command)]} lumps of titanium")

    def game(self):
        print(game_screen_1)
        print(r1 * self.robots)
        print(r2 * self.robots)
        print(r3 * self.robots)
        print(r4 * self.robots)
        print(r5 * self.robots)
        print(game_screen_2.format(titanium=self.titanium_found))
        print()
        print("Your command:", end="")
        self.command = input()
        while True:
            if self.command.lower() == "m":
                print(menu)
                print("Your command:", end="")
                self.command = input()
                if self.command.lower() == "main":
                    return
                elif self.command.lower() == "exit":
                    return "exit"
                elif self.command.lower() == "save":
                    return self.save_exit()
                elif self.command.lower() == "back":
                    ...
            elif self.command.lower() == "back":
                return
            elif self.command.lower() == "save":
                self.save()
            elif self.command.lower() == "ex":
                if self.explore() == "main":
                    return
            elif self.command.lower() == "up":
                self.upgrade()
            else:
                print("Invalid input")
                print("Your command:", end="")
                self.command = input()
                continue
            print(game_screen_1)
            print(r1 * self.robots)
            print(r2 * self.robots)
            print(r3 * self.robots)
            print(r4 * self.robots)
            print(r5 * self.robots)
            print(game_screen_2.format(titanium=self.titanium_found))
            print()
            print("Your command:", end="")
            self.command = input()

    def play(self):
        self.get_name()
        print()
        print(greeting.format(name=self.name))
        while True:
            print(begin)
            print("[Yes] [No] Return to Main[Menu]")
            print()
            print("Your command:", end="")
            self.command = input()
            if self.command.lower() == "yes":
                return self.game()
            elif self.command.lower() == "menu":
                return
            else:
                print("How about now.")

    def start(self):
        # self.create_test_values()
        while True:
            self.animated_print(duskers, self.short_sleep)
            self.animated_print(options, self.short_sleep)
            print()
            self.animated_print("Your Command:", self.short_sleep)
            command = input()
            if command.lower() == "exit":
                return
            elif command.lower() == "new":
                if self.play() == "exit":
                    return
            elif command.lower() == "load":
                if self.load() == "exit":
                    return
            elif command.lower() == "high":
                if self.high() == "exit":
                    return
            elif command.lower() == "help":
                if self.help_me() == "exit":
                    return
            else:
                print("Invalid input")


def main():
    parser = argparse.ArgumentParser(description="Duskers")

    parser.add_argument("seed", help="seed value", nargs="?", default="10")
    parser.add_argument("min", help="min sleep time", type=int, nargs="?", default="0")
    parser.add_argument("max", help="max sleep time", type=int, nargs="?", default="0")
    parser.add_argument("names", help="names separated with '/'", nargs="?", default="High,street/Green,Park/Destroyed,Arch")

    args = parser.parse_args()
    g = Game(args.seed, args.min, args.max, args.names)
    g.start()
    print("Thanks for playing, bye!")


if __name__ == "__main__":
    main()
