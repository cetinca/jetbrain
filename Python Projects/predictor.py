"""Predictor"""

import random

DATA_LENGTH = 100
TRIAD_LIST = ["000", "001", "010", "011", "100", "101", "110", "111"]
CHECK_LIST = ["0", "1"]
triad_dict = {}
balance = 1000


# data for test purposes
# data = "01010010010001010100100101001001101000110010101010101111010010010110100101101010100110101010101010001110011"

def triads(data):
    for triad in TRIAD_LIST:
        zeros = ones = 0
        for i in range(0, len(data) - 4):
            part = data[i:i + 4]
            if part == triad + "0":
                zeros += 1
            elif part == triad + "1":
                ones += 1
        if zeros > ones:
            triad_dict.update({triad: "0"})
        elif ones >= zeros:
            triad_dict.update({triad: "1"})


def get_values(val):
    # val = input()
    data = ""
    if val:
        for v in val:
            if v in CHECK_LIST:
                data += v
    return data


def create_random():  # creates 3 digit prefix for string prediction
    prefix = ""
    for _ in range(3):
        prefix += random.choice(CHECK_LIST)
    return prefix


def predict_string(test):  # creates string with user data
    prediction = create_random()
    for i in range(0, len(test) - 3):
        part = test[i:i + 3]
        for triad in TRIAD_LIST:
            if part == triad:
                prediction += triad_dict[triad]
    return prediction


def compare(string_one, string_two):
    correct_count = 0
    for i in range(len(string_one)):
        if string_one[i] == string_two[i]:
            correct_count += 1
    return correct_count, len(string_one)


def main():
    data = ""
    print("Please give AI some data to learn...")
    print("The current data length is 0, 100 symbols left")
    while True:
        print("Print a random string containing 0 or 1:")
        data += get_values(input())
        if len(data) >= DATA_LENGTH: break
        print(f"The current data length is {len(data)}, {DATA_LENGTH - len(data)} symbols left")

    print()
    print("Final data string:")
    print(data)
    print()
    print("You have $1000. Every time the system successfully predicts your next press, you lose $1.")
    print(("Otherwise, you earn $1. Print 'enough' to leave the game. Let's go!"))
    triads(data)
    print()

    while True:
        global balance
        print("Print a random string containing 0 or 1:")
        test_string = input()
        if test_string:
            if test_string == "enough":
                break
            elif test_string != get_values(test_string):
                continue
        else:
            continue
        predicted_string = predict_string(test_string)
        correct_count, total_count = compare(test_string[3:], predicted_string[3:])
        print("prediction: ")
        print(predicted_string)
        print()
        print(f"Computer guessed right {correct_count} out of {total_count} symbols ("
              f"{round(correct_count / (total_count) * 100, 2)} %)")
        balance = balance - correct_count + (total_count - correct_count)
        # print()
        print(f"Your balance is now ${balance}")
        print()

    print("Game over!")


if __name__ == "__main__":
    main()
