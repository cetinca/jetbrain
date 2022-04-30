# Write your code here
import random
import sys
import csv
from collections import deque

# rock,gun,lightning,devil,dragon,water,air,paper,sponge,wolf,tree,human,snake,scissors,fire

rps = ["rock", "paper", "scissors"]
loser = {"rock": ["paper"], "paper": ["scissors"], "scissors": ["rock"]}
inputs = ["exit", "!exit", "rating", "!rating"]


def get_input():
    global rps, loser
    while True:
        user_input = input()
        if not user_input:
            return
        elif user_input in rps or user_input in inputs:
            return user_input
        else:
            print("Invalid input")


def computer_plays():
    computer_move = random.choice(rps)
    return computer_move


def read_rating(user_name):
    try:
        with open("rating.txt", "r", newline="", encoding="utf-8") as file:
            new_file = list(file.readlines())
            for n in new_file:
                name, score = n.strip().split(" ")
                if name == user_name:
                    return int(score)
                    break
    except:
        return 0

def prepare_list(_list):
    global rps, loser
    rps = deque(_list.split(","))
    length = int((len(rps) - 1) / 2)
    loser = {}
    for i in range(len(rps)):
        win_over = []
        for j in range(1, length + 1):
            win_over.append(rps[j])
            loser.update({rps[0]: win_over})
        rps.rotate(-1)
    print(loser)


def main():
    print("Enter your name:")
    player_name = input()
    print(f"Hello, {player_name}")
    new_list = input()
    if new_list:
        prepare_list(new_list)
    print("Okay, let's start")
    rating = read_rating(player_name) or 0
    while True:
        player = get_input()
        computer = computer_plays()
        if player == "!exit" or player == "exit":
            sys.exit()
        elif player == "rating" or player == "!rating":
            print(rating)
        elif player == computer:
            rating += 50
            print(f"There is a draw {player}")
        elif computer in loser[player]:
            print(f"Sorry, but the computer chose {computer}")
        else:
            rating += 100
            print(f"Well done. The computer chose {computer} and failed")

if __name__ == main():
    main()
