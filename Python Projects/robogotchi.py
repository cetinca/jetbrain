# Write your code here
import random
import sys
import random


class Robot:
    def __init__(self, name):
        self.robot_name = name
        self.level_of_battery = 100
        self.level_of_overheat = 0
        self.level_of_skills = 0
        self.level_of_boredom = 0
        self.level_of_rust = 0


class Numbers:
    def __init__(self):
        self.goal = 0
        self.robot_value = 0
        self.user_value = 0
        self.robot_score = 0
        self.user_score = 0
        self.draws = 0

    def generate_goal(self):
        self.goal = random.randint(0, 1000000)

    def generate_robot_value(self):
        self.robot_value = random.randint(0, 1000000)
        # return self.robot_value

    def get_input(self):
        print()
        print("What is your number?")
        user_input = input()
        if user_input == "exit game":
            return "exit game"
        elif user_input.isdigit():
            user_input = int(user_input)
            if 0 <= user_input <= 1000000:
                self.user_value = user_input
                return "turn_played"
            else:
                return "Invalid input! The number can't be bigger than 1000000."
        elif user_input.isalpha():
            return "A string is not a valid input!"
        elif user_input.startswith("-") and user_input[1:].isdigit():
            return "The number can't be negative!"
        else:
            return "A string is not a valid input!"

    def compare_values(self):
        if abs(self.goal - self.user_value) < abs(self.goal - self.robot_value):
            self.user_score += 1
            return "You won!"
        elif abs(self.goal - self.user_value) > abs(self.goal - self.robot_value):
            self.robot_score += 1
            return "The robot won!"
        else:
            self.draws += 1
            return "Draw!"

    def print_game_score(self):
        print()
        print(f"You won: {self.user_score},")
        print(f"The robot won: {self.robot_score},")
        print(f"Draws: {self.draws}.")

    def print_turn_score(self):
        print()
        print(f"The robot entered the number {self.robot_value}.")
        print(f"The goal number is {self.goal}.")
        print(self.compare_values())


class RockPaper(Numbers):
    def __init__(self):
        super().__init__()
        self.selections = ["rock", "paper", "scissors"]

    def generate_goal(self):
        self.goal = random.choice(self.selections)

    def generate_robot_value(self):
        self.robot_value = random.choice(self.selections)
        # return self.robot_value

    def get_input(self):
        print()
        print("What is your move?")
        user_input = input()
        if user_input == "exit game":
            return "exit game"
        elif user_input not in self.selections:
            return "No such option! Try again!"
        else:
            self.user_value = user_input
            return "turn_played"

    def compare_values(self):
        if self.user_value == self.robot_value:
            self.draws += 1
            return "It's a draw!"
        elif self.user_value == "rock" and self.robot_value == "scissors":
            self.user_score += 1
            return "You won!"
        elif self.user_value == "paper" and self.robot_value == "rock":
            self.user_score += 1
            return "You won!"
        elif self.user_value == "scissors" and self.robot_value == "paper":
            self.user_score += 1
            return "You won!"
        else:
            self.robot_score += 1
            return "The robot won!"

    def print_turn_score(self):
        print()
        print(f"The robot chose {self.robot_value}.")
        print(self.compare_values())


def play_game(pg):
    while True:
        pg.generate_goal()
        pg.generate_robot_value()
        play_turn = pg.get_input()
        if play_turn == "exit game":
            break
        elif play_turn == "turn_played":
            pg.print_turn_score()
        else:
            print(play_turn)  # if user input is not correct, returns the error.


def select_game(r):
    boredom = r.level_of_boredom
    overheat = r.level_of_overheat
    while True:
        print()
        print("Which game would you like to play?")
        game_selection = input()
        if game_selection.lower() == "Rock-paper-scissors".lower():
            pg = RockPaper()
            play_game(pg)
            break
        elif game_selection.lower() == "Numbers".lower():
            pg = Numbers()
            play_game(pg)
            break
        else:
            print("Please choose a valid option: Numbers or Rock-paper-scissors?")
    if r.level_of_boredom <= 20:
        r.level_of_boredom = 0
        r.level_of_overheat += 10
    else:
        r.level_of_boredom -= 20
        r.level_of_overheat += 10
    if r.level_of_overheat == 100:
        print()
        print(f"The level of overheat reached 100, {r.robot_name} has blown up! Game over. Try again?")
        sys.exit()
    pg.print_game_score()
    print()
    print(f"{r.robot_name}'s level of boredom was {boredom}. Now it is {r.level_of_boredom}.")
    print(f"{r.robot_name}'s level of overheat was {overheat}. Now it is {r.level_of_overheat}.")
    if r.level_of_boredom == 0: print(f"{r.robot_name} is in a great mood!")
    del pg


def print_stats(r):
    print()
    print(f"{r.robot_name}'s stats are: battery is {r.level_of_battery},")
    print(f"overheat is {r.level_of_overheat},")
    print(f"skill level is {r.level_of_skills},")
    print(f"boredom is {r.level_of_boredom}.")
    print(f"rust is {r.level_of_rust}.")


def recharge(r):
    overheat = r.level_of_overheat
    battery = r.level_of_battery
    boredom = r.level_of_boredom
    if r.level_of_battery == 100:
        print(f"{r.robot_name} is charged!")
    else:
        r.level_of_battery += 10
        if r.level_of_overheat != 0: r.level_of_overheat -= 5
        if r.level_of_boredom != 100: r.level_of_boredom += 5
        print(f"{r.robot_name}'s level of overheat was {overheat}. Now it is {r.level_of_overheat}.")
        print(f"{r.robot_name}'s level of the battery was {battery}. Now it is {r.level_of_battery}.")
        print(f"{r.robot_name}'s level of boredom was {boredom}. Now it is {r.level_of_boredom}.")
    print()
    print(f"{r.robot_name} is recharged")


def sleeps(r):
    overheat = r.level_of_overheat
    if r.level_of_overheat == 0:
        print(f"{r.robot_name} is cool!")
    elif r.level_of_overheat <= 20:
        r.level_of_overheat = 0
        print()
        print(f"{r.robot_name}'s level of overheat was {overheat}. Now it is 0.")
        print()
        print(f"{r.robot_name} is cool!")
    else:
        r.level_of_overheat -= 20
        print(f"{r.robot_name} cooled off!")
        print(f"{r.robot_name}'s level of overheat was {overheat}. Now it is {r.level_of_overheat}.")


def check_status(r):
    print()
    if r.level_of_overheat >= 100:
        print(f"The level of overheat reached 100, {r.robot_name} has blown up! Game over. Try again?")
        sys.exit()
    if r.level_of_rust >= 100:
        print(f"{r.robot_name} is too rusty! Game over. Try again?")
        sys.exit()
    elif r.level_of_battery == 0:
        print(f"The level of the battery is 0, {r.robot_name} needs recharging!")
        return "battery"
    elif r.level_of_boredom == 100:
        print(f"{r.robot_name} is too bored! {r.robot_name} needs to have fun!")
        return "boredom"


def oil(r):
    rust = r.level_of_rust
    if r.level_of_rust == 0:
        print(f"{r.robot_name} is fine, no need to oil!")
    elif r.level_of_rust < 20:
        r.level_of_rust = 0
        print(
            f"{r.robot_name}'s level of rust was {rust}. Now it is {r.level_of_rust}. {r.robot_name} is less "
            f"rusty!"
            )
    else:
        r.level_of_rust -= 20
        print(
            f"{r.robot_name}'s level of rust was {rust}. Now it is {r.level_of_rust}. {r.robot_name} is less "
            f"rusty!"
            )


def unpleasant_event(r):
    print()
    events = {0: f"Oh no, {r.robot_name} stepped into a puddle!", 1: f"Guess what! {r.robot_name} fell into the pool!"}
    if r.level_of_battery < 10:
        r.level_of_rust += 50
        print(events[1])
    elif r.level_of_battery < 30:
        r.level_of_rust += 10
        print(events[0])


def work(r):
    boredom = r.level_of_boredom
    overheat = r.level_of_overheat
    battery = r.level_of_battery
    rust = r.level_of_rust
    if r.level_of_skills < 50:
        print(f"{r.robot_name} has got to learn before working!")
        return
    r.level_of_boredom += 10
    r.level_of_overheat += 10
    r.level_of_battery -= 10
    unpleasant_event(r)
    print()
    print(f"{r.robot_name}'s level of boredom was {boredom}. Now it is {r.level_of_boredom}.")
    print(f"{r.robot_name}'s level of overheat was {overheat}. Now it is {r.level_of_overheat}.")
    print(f"{r.robot_name}'s level of the battery was {battery}. Now it is {r.level_of_battery}.")
    if rust != r.level_of_rust:
        print(f"{r.robot_name}'s level of rust was {rust}. Now it is {r.level_of_rust}.")
    print()
    print(f"{r.robot_name} did well!")


def learn(r):
    print()
    skill = r.level_of_skills
    overheat = r.level_of_overheat
    battery = r.level_of_battery
    boredom = r.level_of_boredom
    rust = r.level_of_rust
    if r.level_of_skills == 100:
        print(f"There's nothing for {r.robot_name} to learn!.")
    else:
        r.level_of_skills += 10
        r.level_of_overheat += 10
        r.level_of_battery -= 10
        r.level_of_boredom += 5
        unpleasant_event(r)
        print(f"{r.robot_name}'s level of skill was {skill}. Now it is {r.level_of_skills}.")
        print(f"{r.robot_name}'s level of overheat was {overheat}. Now it is {r.level_of_overheat}.")
        print(f"{r.robot_name}'s level of the battery was {battery}. Now it is {r.level_of_battery}.")
        print(f"{r.robot_name}'s level of boredom was {boredom}. Now it is {r.level_of_boredom}.")
        if rust != r.level_of_rust:
            print(f"{r.robot_name}'s level of rust was {rust}. Now it is {r.level_of_rust}.")
        print()
        print(f"{r.robot_name} has become smarter!")


def main():
    print("How will you call your robot?")
    robot_name = input()
    r = Robot(robot_name)

    interactions = {
        "msg"     : f"Available interactions with {robot_name}:",
        "exit"    : "exit - Exit",
        "info"    : "info - Check the vitals",
        "work"    : "work - Work",
        "play"    : "play - Play",
        "oil"     : "oil - Oil",
        "recharge": "recharge - Recharge",
        "sleep"   : "sleep - Sleep mode",
        "learn"   : "learn - Learn skills"
        }

    while True:
        status = check_status(r)
        print()
        for v in interactions.values():
            print(v)
        print()
        print("Choose:")
        user_input = input()
        if user_input not in interactions.keys():
            print("Invalid input, try again!")
        elif user_input == "exit":
            break
        elif user_input == "info" and not status:
            print_stats(r)
        elif user_input == "recharge" and status != "boredom":
            recharge(r)
        elif user_input == "play" and status != "battery":
            select_game(r)
        elif user_input == "sleep" and not status:
            sleeps(r)
        elif user_input == "learn" and not status:
            learn(r)
        elif user_input == "work" and not status:
            work(r)
        elif user_input == "oil" and not status:
            oil(r)

    print()
    print("Game over")


if __name__ == "__main__":
    main()
