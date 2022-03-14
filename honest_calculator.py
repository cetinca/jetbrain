# write your code here
import sys
import math

msg_0 = "Enter an equation"
msg_1 = "Do you even know what numbers are? Stay focused!"
msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"
msg_3 = "Yeah... division by zero. Smart move..."
msg_4 = "Do you want to store the result? (y / n):"
msg_5 = "Do you want to continue calculations? (y / n):"
msg_6 = " ... lazy"
msg_7 = " ... very lazy"
msg_8 = " ... very, very lazy"
msg_9 = "You are"
msg_10 = "Are you sure? It is only one digit! (y / n)"
msg_11 = "Don't be silly! It's just one number! Add to the memory? (y / n)"
msg_12 = "Last chance! Do you really want to embarrass yourself? (y / n)"


def isfloat(number):
    try:
        float(number)
        return True
    except ValueError:
        return False


def is_one_digit(v):
    if (-10 < float(v) < 10) and math.modf(float(v))[0] == 0:  # checking is fractional part is zero.
        return True
    else:
        return False


def check(v1, v2, v3):
    msg = ""
    if is_one_digit(v1) and is_one_digit(v2):
        msg = msg + msg_6
    if (float(v1) == 1 or float(v2) == 1) and v3 == "*":
        msg = msg + msg_7
    if (float(v1) == 0 or float(v2) == 0) and (v3 == "*" or v3 == "+" or v3 == "-"):
        msg = msg + msg_8
    if msg != "":
        msg = msg_9 + msg
        print(msg)
        return
    else:
        return


memory = 0

while True:
    while True:
        print(msg_0)
        entered = input()
        x, oper, y = entered.split()

        if x == "M":
            x = memory
        if y == "M":
            y = memory

        if not isfloat(x) or not isfloat(y):
            print(msg_1)
            continue
        elif oper not in ["+", "-", "*", "/"]:
            print(msg_2)
            continue

        check(x, y, oper)

        if oper == "+":
            result = float(x) + float(y)
            break
        elif oper == "-":
            result = float(x) - float(y)
            break
        elif oper == "*":
            result = float(x) * float(y)
            break
        elif oper == "/" and float(y) != 0:
            result = float(x) / float(y)
            break
        else:
            print(msg_3)

    print(result)
    print(msg_4)
    answer = input()
    if answer == "y":
        if is_one_digit(result):
            msg_index = 10
            while True:
                print(eval(f"msg_{msg_index}"))
                answer = input()
                if answer == "y":
                    msg_index += 1
                    if msg_index == 13:
                        memory = result
                        break
                else:
                    break
        else:
            memory = result

    while True:
        print(msg_5)
        answer = input()
        if answer == "y":
            break
        else:
            sys.exit()
