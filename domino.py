# Write your code here
import random

doubles = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6]]
domino_set = []
number_list = [str(x) for x in range(-9, 10)]


def create_set():
    for i in range(7):
        for j in range(i, 7):
            domino_set.append([i, j])
    random.shuffle(domino_set)
    return domino_set


def find_beginner(player, computer, domino_snake):
    p = c = beginner = ""
    for double in doubles:
        if double in player:
            p = double
        elif double in computer:
            c = double

    if not p and not c:
        return
    elif p and not c:
        player.remove(p)
        domino_snake.append(p)
        beginner = "computer"
    elif not p and c:
        computer.remove(c)
        domino_snake.append(c)
        beginner = "player"
    elif p[0] > c[0]:
        player.remove(p)
        domino_snake.append(p)
        beginner = "computer"
    elif c[0] > p[0]:
        computer.remove(c)
        domino_snake.append(c)
        beginner = "player"
    return player, computer, domino_snake, beginner


def print_board(stock_pieces, player, computer, domino_snake):
    print(70 * "=")
    print(f"Stock size: {len(stock_pieces)}")
    print(f"Computer pieces: {len(computer)}")
    print()
    if len(domino_snake) > 6:
        print(domino_snake[0], domino_snake[1], domino_snake[2], "...", domino_snake[-3], domino_snake[-2],
              domino_snake[-1])
        print()
    else:
        for d in domino_snake:
            print(d, end="")
        print(f"\n")
    print("Your pieces:")
    for i in range(len(player)):
        print(f"{i + 1}:{player[i]}")
    print()


def check_winner(player, computer, domino_snake):
    if len(player) == 0:
        return "player"
    elif len(computer) == 0:
        return "computer"
    elif len(domino_snake) > 1:
        if domino_snake[0][0] == domino_snake[-1][-1]:
            number = domino_snake[0][0]
            count_number = 0
            for d in domino_snake:
                if d[0] == number:
                    count_number += 1
                if d[1] == number:
                    count_number += 1
            if count_number == 8:
                print(domino_snake)
                return "draw"


def play_player(player, computer, stock_pieces, domino_snake):
    while True:
        player_command = input()
        if player_command not in number_list:
            print("Invalid input. Please try again.")
            return
        elif len(player) < abs(int(player_command)):
            print("Invalid input. Please try again.")
            return
        elif int(player_command) == 0 and len(stock_pieces) > 0:
            domino = stock_pieces.pop()
            player.append(domino)
        elif int(player_command) < 0:
            domino = player[abs(int(player_command)) - 1]
            snake = domino_snake[0]
            if snake[0] == domino[1]:
                player.pop(abs(int(player_command)) - 1)
                domino_snake.insert(0, domino)
            elif snake[0] == domino[0]:
                domino = domino[::-1]
                player.pop(abs(int(player_command)) - 1)
                domino_snake.insert(0, domino)
            else:
                print("Illegal move. Please try again.")
                continue
        elif int(player_command) >= 0:
            domino = player[abs(int(player_command)) - 1]
            snake = domino_snake[-1]
            if snake[-1] == domino[0]:
                player.pop(abs(int(player_command)) - 1)
                domino_snake.append(domino)
            elif snake[-1] == domino[1]:
                domino = domino[::-1]
                player.pop(abs(int(player_command)) - 1)
                domino_snake.append(domino)
            else:
                print("Illegal move. Please try again.")
                continue
        else:
            print("Illegal move. Please try again.")
            continue
        print_board(stock_pieces, player, computer, domino_snake)
        status = "computer"
        return player, computer, stock_pieces, domino_snake, status


def find_sequence(computer, domino_snake):
    domino_computer = computer + domino_snake
    score_dict = {}
    play_sequence = []
    for b in domino_computer:
        number_list.extend(b)
    number_set = set(number_list)
    for n in number_set:
        score_dict.update({n: number_list.count(n)})
    score = 0
    for c in computer:
        new_score = score_dict[c[0]] + score_dict[c[1]]
        if score > new_score:
            play_sequence.append(c)
            score = new_score
        else:
            play_sequence.insert(0, c)
            score = new_score
    return play_sequence


def play_computer(player, computer, stock_pieces, domino_snake):
    while True:
        play_list = find_sequence(computer, domino_snake)
        len_computer = len(computer)
        for domino in play_list:
            snake = domino_snake[0]
            if snake[0] == domino[1]:
                computer.remove(domino)
                domino_snake.insert(0, domino)
                break
            elif snake[0] == domino[0]:
                computer.remove(domino)
                domino = domino[::-1]
                domino_snake.insert(0, domino)
                break
            snake = domino_snake[-1]
            if snake[-1] == domino[0]:
                computer.remove(domino)
                domino_snake.append(domino)
                break
            elif snake[-1] == domino[1]:
                computer.remove(domino)
                domino = domino[::-1]
                domino_snake.append(domino)
                break
        if (len_computer == len(computer)) and len(stock_pieces) > 0:
            domino = stock_pieces.pop()
            computer.append(domino)
        input()
        print_board(stock_pieces, player, computer, domino_snake)
        status = "player"
        return player, computer, stock_pieces, domino_snake, status


def main():
    while True:
        create_set()
        domino_snake = []
        player, computer, stock_pieces = domino_set[0:7], domino_set[7:14], domino_set[14:]

        who_begins = find_beginner(player, computer, domino_snake)

        if who_begins:
            player, computer, domino_snake, status = who_begins[0], who_begins[1], who_begins[2], who_begins[3]
            break

    print_board(stock_pieces, player, computer, domino_snake)

    while True:
        winner = check_winner(player, computer, domino_snake)
        if winner:
            break

        if status == "player":
            print(f"Status: It's your turn to make a move. Enter your command.")
            played = play_player(player, computer, stock_pieces, domino_snake)
            if played:
                player, computer, stock_pieces, domino_snake, status = played
        elif status == "computer":
            print(f"Status: Computer is about to make a move. Press Enter to continue...")
            played = play_computer(player, computer, stock_pieces, domino_snake)
            if played:
                player, computer, stock_pieces, domino_snake, status = played

    if winner == "player":
        print("Status: The game is over. You won!")
    elif winner == "computer":
        print("Status: The game is over. The computer won!")
    elif winner == "draw":
        print("The game is over. It'  s a draw!")


if __name__ == "__main__":
    main()
