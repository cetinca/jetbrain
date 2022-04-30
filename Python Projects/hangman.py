"""JetBrains Hangman Game Project"""

import random


def play_game():
    misses = ""
    tries = 8
    word_list = ['python', 'java', 'kotlin', 'javascript']
    random_word = word_list[random.randint(0, 3)]
    # random_word = "java"
    letters = list(random_word)
    new_letters = list(len(letters) * "-")
    print("H A N G M A N")
    print()

    while True:
        if "-" not in new_letters:
            print(random_word)
            print("You guessed the word!")
            print("You survived!")
            break
        print("".join(new_letters))
        user_input = input("Input a letter: ")

        if user_input == random_word:
            print("You guessed the word!")
            print("You survived!")
            break
        elif len(user_input) != 1:
            print("You should input a single letter")
        # elif not user_input.isalpha():
        #     print("You should input a single letter")
        elif not user_input.islower():
            print("Please enter a lowercase English letter")
        elif user_input in letters and user_input not in new_letters:
            for k, v in enumerate(letters):
                if v == user_input:
                    new_letters[k] = v
        elif user_input in new_letters:
            print("You've already guessed this letter")
        elif user_input not in new_letters and user_input in misses:
            print("You've already guessed this letter")
        elif user_input not in new_letters:
            print("That letter doesn't appear in the word")
            misses += user_input
            tries -= 1
        if tries == 0:
            print("You lost!")
            break
        print()


while True:
    print('Type "play" to play the game, "exit" to quit:')
    usr = input()
    if usr == "play":
        play_game()
    elif usr == "exit":
        break
