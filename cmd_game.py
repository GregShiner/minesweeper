from board import Board

board = Board(10, 10)
print("Welcome to Minesweeper!")


def validate_square(r, c):
    if r.isdigit() and c.isdigit():
        r = int(r)
        c = int(c)
        if r in range(board.size) and c in range(board.size):
            return True
        else:
            print("Coordinates not within board")
    else:
        print("Input invalid")
    return False


def lose(mineRow, mineCol):
    board.board[mineRow][mineCol].revealed = True
    print(board)
    mine = (mineRow, mineCol)
    print("You lose, coordinates ", str(mine), "had a mine")


def win():
    print(board)
    print("You win! All unrevealed tiles remaining are mines")


def startGame():
    print(board)

    while True:
        command = input("Reveal or flag a tile? ")
        if command.lower() == 'reveal' or command.lower() == 'r':
            row = input("Which row? (0 - " + str(board.size - 1) + ") ")
            col = input("Which column? (0 - " + str(board.size - 1) + ") ")
            if validate_square(row, col):
                if not board.left_click(int(row), int(col)):
                    lose(int(row), int(col))
                    break
                elif board.num_revealed + board.num_mines == board.size * board.size:
                    win()
                    break
                else:
                    print(board)
        elif command.lower() == 'flag' or command.lower() == 'f':
            row = input("Which row? (0 - " + str(board.size - 1) + ") ")
            col = input("Which column? (0 - " + str(board.size - 1) + ") ")
            if validate_square(row, col):
                board.right_click(int(row), int(col))
                print(board)
        else:
            print("Invalid command")


while True:
    size = input("How many rows/columns would you like? (x to escape) ")
    if size.isdigit():
        mines = input("How many mines would you like? ")
        if mines.isdigit():
            size = int(size)
            mines = int(mines)
            if mines < size * size:
                board = Board(size, mines)
                startGame()

                cont = input("Play again? (y/n) ")
                if cont == 'y':
                    print("OK!")
                elif cont == 'n':
                    print("Ok, terminating...")
                else:
                    print("Input invalid, terminating...")
            else:
                print("Too many mines for board size")
        else:
            print("Invalid input")
    elif size == 'x':
        print("Terminating...")
        break
    else:
        print("Invalid input")
