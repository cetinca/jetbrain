"""Coffee Machine"""

import csv
import sys

ingredients = {
    "espresso"  : {"water": 250, "milk": 0, "coffee beans": 16, "disposable cups": 1, "money": -4},
    "latte"     : {"water": 350, "milk": 75, "coffee beans": 20, "disposable cups": 1, "money": -7},
    "cappuccino": {"water": 200, "milk": 100, "coffee beans": 12, "disposable cups": 1, "money": -6}
    }
units = {"water": "ml", "milk": "ml", "coffee beans": "grams", "disposable cups": "pcs", "money": "$"}
inventory = {"water": 400, "milk": 540, "coffee beans": 120, "disposable cups": 9, "money": 550}
coffee_amount = {"water": 0, "milk": 0, "coffee beans": 0}
coffee_order = 0
coffe_type = {"1": "espresso", "2": "latte", "3": "cappuccino"}


def entry():
    print("Starting to make a coffee")
    print("Grinding coffee beans")
    print("Boiling water")
    print("Mixing boiled water with crushed coffee beans")
    print("Pouring coffee into the cup")
    print("Pouring some milk into the cup")
    print("Coffee is ready!")


def fill_material():
    for k, v in inventory.items():
        if k != "money":
            print(f"Write how many {units[k]} of {k} you want to add:")
            inventory[k] += int(input())
    # print("Write how many ml of water you want to add:")
    # inventory["water"] += int(input())
    # print("Write how many ml of milk you want to add:")
    # inventory["milk"] += int(input())
    # print("Write how many grams of coffee beans you want to add:")
    # inventory["coffee beans"] += int(input())
    # print("Write how many disposable coffee cups you want to add:")
    # inventory["disposable cups"] += int(input())


def inventory_print():
    print("The coffee machine has:")
    for k, v in inventory.items():
        if k != "money":
            print(f"{v} of {k}")
        else:
            print(f"${v} of {k}")


def order():
    global coffee_order
    print("Write how many cups of coffee you will need:")
    coffee_order = int(input())


def check_ingredients(_materials):
    for k, v in _materials.items():
        if inventory[k] < v:
            print(f"Sorry, not enough {k}!")
            return False
        return True


def calculate_coffee():
    for k, v in inventory.items():
        coffee_amount[k] = v // ingredients[k]

    coffee_can_be_made = min(coffee_amount.values())

    if coffee_can_be_made < coffee_order:
        print(f"No, I can make only {coffee_can_be_made} cups of coffee")
    elif coffee_can_be_made == coffee_order:
        print(f"Yes, I can make that amount of coffee")
    else:
        print(f"Yes, I can make that amount of coffee (and even {coffee_can_be_made - coffee_order} more than that)")


def main():
    while True:
        print()
        print("Write action (buy, fill, take, remaining, exit):")
        action = input()
        if action == "exit":
            sys.exit()
        elif action == "remaining":
            print()
            inventory_print()
        elif action == "fill":
            print()
            fill_material()
        elif action == "take":
            print(f'I gave you {units["money"]}{inventory["money"]}')
            inventory["money"] = 0
        elif action == "buy":
            print()
            print(f"What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:")
            coffee_id = input()
            if coffee_id == "back":
                continue
            _type = coffe_type[coffee_id]
            materials = ingredients[_type]
            if check_ingredients(materials):
                print("I have enough resources, making you a coffee!")
                for k, v in materials.items():
                    inventory[k] -= v


if __name__ == "__main__":
    main()
