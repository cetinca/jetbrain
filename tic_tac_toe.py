"""tic tac toe game"""

from collections import deque

patterns = deque(["11", "12", "13", "21", "22", "23", "31", "32", "33", "11",
                  "21",
                  "31", "12", "22", "32", "13", "23", "33", "11", "22", "33",
                  "13",
                  "22", "31"])

board = {}
sub_list = ["1", "2", "3"]
select_player = 0

for i in sub_list:
    for j in sub_list:
        board.update({i + j: "_"})


# board = {'11': 'X', '12': 'X', '13': '_', '21': '_', '22': '_', '23': '_',
#          '31': '_', '32': '_', '33': '_'}
#
# board = {'11': 'X', '12': '0', '13': 'X', '21': 'O', '22': 'X', '23': 'O',
#          '31': '_', '32': 'X', '33': 'O'}

def print_board():
    print("---------")
    for i in sub_list:
        print("| ", end="")
        for j in sub_list:
            if board[i + j] == "_":
                print(" ", end=" ")
            else:
                print(board[i + j], end=" ")
        print("|")
    print("---------")


def get_input():
    while True:
        print("Enter the coordinates: ", end="")
        row, column = input().split(" ")
        if select_player % 2 == 0:
            player = "X"
        else:
            player = "O"
        if not row.isnumeric() or not column.isnumeric():
            print("You should enter numbers!")
        elif row not in ["1", "2", "3"] or column not in ["1", "2", "3"]:
            print("Coordinates should be from 1 to 3!")
        elif board[row + column] != "_":
            print("This cell is occupied! Choose another one!")
        else:
            board.update({row + column: player})
            return


def check_score():
    for _ in range(len(patterns)):
        check_game = board[patterns[0]] + board[patterns[1]] + board[
            patterns[2]]
        patterns.rotate(-3)
        if check_game.count("X") == 3:
            return "X wins"
        elif check_game.count("O") == 3:
            return "O wins"
    if "_" not in board.values():
        return "Draw"


while True:
    print_board()
    get_input()
    result = check_score()
    select_player += 1

    if result:
        print_board()
        print(result)
        break  # or sys.exit()
