"""Bill Splitter"""
import random

friends = {}


def count_friends(size):
    print()
    print("Enter the name of every friend (including you)")
    for _ in range(size):
        friends.update({input(): 0})


def calculate_bill(size):
    print()
    print("Enter total bill value:")
    total_bill = int(input())
    print()
    print('Do you want to use "Who is lucky?" feature? Write Yes/No:')
    lucky_mode = input()

    if lucky_mode == "Yes":
        lucky = random.choice(list(friends.keys()))
        print()
        print(f"{lucky} is the lucky one!")
        bill = round(total_bill / (size - 1), 2)
        for k, v in friends.items():
            friends.update({k: bill})
        friends.update({lucky: 0})

    else:
        print()
        print("No one is going to be lucky")
        bill = round(total_bill / size, 2)
        for k, v in friends.items():
            friends.update({k: bill})


def main():
    print()
    print("Enter the number of friends joining (including you):")
    party_size = input()

    if party_size:
        if int(party_size) <= 0:
            print("No one is joining for the party")
        else:
            party_size = int(party_size)
            count_friends(party_size)
            calculate_bill(party_size)
            print()
            print(friends)
    else:
        print("No one is joining for the party")


main()
