import math
import sys
from collections import deque

nums = {}
operators = {"+", "-", "*", "/", "^"}
operator_higher = {"-": "/*^", "+": "/*^", "/": "^", "*": "^"}
operator_equal = {"+": "-+", "-": "-+", "*": "/*", "/": "/*"}
invalid_exp = ["**", "^^", "^*", "^*", "//", "/*", "*/", "/^", "^/"]
token = []


def trim_chars(_collection):
    entered = _collection
    # if any([True for e in entered if e in operators]):
    #     for i in range(math.ceil(math.log(len(entered), 2))):
    entered = entered.replace(" ", "")
    entered = entered.replace("--", "+")
    entered = entered.replace("++", "+")
    entered = entered.replace("+-", "-")
    entered = entered.replace("-+", "-")
    return entered


def check_brackets(_collection):  # from internet
    _stack = []
    open_list = ["[", "{", "("]
    close_list = ["]", "}", ")"]
    for i in _collection:
        if i in open_list:
            _stack.append(i)
        elif i in close_list:
            pos = close_list.index(i)
            if ((len(_stack) > 0) and
                    (open_list[pos] == _stack[len(_stack) - 1])):
                _stack.pop()
            else:
                return False
    if len(_stack) == 0:
        return True
    else:
        return False


def to_postfix(_collection):
    _queue = []
    _stack = []
    global operators
    for item in _collection:
        if item.isdigit() or item.isalpha():
            _queue.append(item)
        elif item in operators and (len(_stack) == 0 or _stack[-1] == "("):
            _stack.append(item)
        elif item in operators and item in operator_higher[_stack[-1]]:
            _stack.append(item)
        elif item in operators and (_stack[-1] in operator_higher[item] or _stack[-1] in operator_equal[item]):
            while True:
                if len(_stack) > 0 and (_stack[-1] in operator_higher[item] or _stack[-1] in operator_equal[item]):
                    _queue.append(_stack.pop())
                else:
                    _stack.append(item)
                    break
        elif item == "(":
            _stack.append(item)
        elif item == ")":
            while True:
                if _stack[-1] != "(":
                    _queue.append(_stack.pop())
                else:
                    _stack.pop()
                    break
    while len(_stack):
        _queue.append(_stack.pop())
    return _queue


def create_token(_collection):
    _token = []
    entered = collection
    while len(entered):
        i = 0
        while True:
            try:
                if entered[i].isdigit() and not entered[i + 1].isdigit():
                    _token.append(entered[:i + 1])
                    entered = entered[i + 1:]
                    break
                elif not entered[i].isdigit():
                    _token.append(entered[:i + 1])
                    entered = entered[i + 1:]
                    break
                i += 1
            except:
                _token.append(entered)
                entered = []
                break
    return _token


def do_math(_operator, num_1, num_2):
    num_1 = int(num_1)
    num_2 = int(num_2)
    if _operator == "+":
        return num_1 + num_2
    elif _operator == "-":
        return num_1 - num_2
    elif _operator == "*":
        return num_1 * num_2
    elif _operator == "/":
        return num_1 / num_2
    elif _operator == "^":
        return num_1 ** num_2


def calculate(_collection):
    _stack = []
    for item in _collection:
        if item.isdigit():
            _stack.append(item)
        elif item in operators:
            b = _stack.pop()
            a = _stack.pop()
            _stack.append(do_math(item, a, b))
    return _stack[-1]


def get_user_input():
    user_input = trim_chars(input())
    count_e_sign = user_input.count("=")
    if user_input == "":
        pass
    elif user_input == "/help":
        print("The program calculates the sum of numbers")
    elif user_input == "/exit":
        print("Bye!")
        sys.exit()
    elif user_input[0] == "/":
        print("Unknown command")
    elif user_input.isdigit() or (user_input[0] == "-" and user_input[1:].isdigit()):
        print(user_input)
    elif any([True for inv in invalid_exp if inv in user_input]):
        print("Invalid expression")
    elif not check_brackets(user_input):
        print("Invalid expression")
    elif user_input.isalpha():
        try:
            print(nums[user_input])
        except:
            print("Unknown variable")
    elif user_input.isalnum():
        print("Invalid identifier")
    elif count_e_sign > 1:
        print("Invalid assignment")
    elif count_e_sign == 1:
        var, num = user_input.split("=")
        if var.isalpha() and num.isdigit():
            nums.update({var: num})
        elif var.isalpha and num in nums.keys():
            num = nums[num]
        else:
            print("Invalid expression")
    else:  # converts variable to numbers
        temp = ""
        for v in user_input:
            try:
                temp += nums[v]
            except:
                temp += v
        return temp


while True:
    collection = get_user_input()
    if not collection:
        continue
    else:
        token = create_token(collection)
        # print(token)
        result = to_postfix(token)
        # print(result)
        print(calculate(result))
