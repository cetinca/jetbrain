# write your code here
import random

"""
from other students good examples

operations_handler = {'+': lambda a, b: a + b, '-': lambda a, b: a - b, '*': lambda a, b: a * b}
x, operation, y = input().split()
print(operations_handler[operation](int(x), int(y)))

user_input = input()
print(eval(user_input))
"""


def addition(_num_one, _num_two):
    result = _num_one + _num_two
    return result


def subtraction(_num_one, _num_two):
    result = _num_one - _num_two
    return result


def multiplication(_num_one, _num_two):
    result = _num_one * _num_two
    return result


def division(_num_one, _num_two):
    result = _num_one / _num_two
    return result


def get_user_input(_question):
    while True:
        print(_question)
        try:
            user_input = int(input())
        except:
            print("Wrong format! try again.")
        else:
            return user_input


def simple_operations():
    num_one = random.randint(2, 9)
    num_two = random.randint(2, 9)
    operator = random.choice([k for k in operation.keys()])
    func = operation[operator]
    result = func(num_one, num_two)
    question = f"{num_one} {operator} {num_two}"
    user_input = get_user_input(question)
    if user_input == result:
        return True


def integral_squares():
    random_number = random.randint(11, 29)
    user_input = get_user_input(random_number)
    if user_input == random_number ** 2:
        return True


def ask_level():
    while True:
        print("Which level do you want? Enter a number:")
        print("1 - simple operations with numbers 2-9")
        print("2 - integral squares of 11-29")
        user_input = input()
        if user_input not in ["1", "2"]:
            print("Incorrect format.")
            continue
        else:
            return user_input


operation = {"+": addition, "-": subtraction, "*": multiplication}
levels = {"1": "(simple operations with numbers 2-9)", "2": "(integral squares of 11-29)"}


def main():
    score = 0
    level = ask_level()
    result = False
    for i in range(5):
        if level == "1":
            result = simple_operations()
        elif level == "2":
            result = integral_squares()
        if result:
            print("Right!")
            score += 1
        else:
            print("Wrong!")

    print(f"Your mark is {score}/5.")
    print("Would you like to save your result to the file?")
    save_to_file = input().lower()
    if save_to_file == "yes" or save_to_file == "y":
        print("What is your name?")
        user_name = input()
        with open("results.txt", "a") as file:
            file.write(f"{user_name}: {score}/5 in level {level} {levels[level]}." + "\n")
            print('The results are saved in "results.txt".')


if __name__ == "__main__":
    main()
