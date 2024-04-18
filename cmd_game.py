from board import Board

board = Board(10, 10)
print(board)

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
    print(board)
    mine = (mineRow, mineCol)
    print("You lose, coordinates ", str(mine), "had a mine")


while True:
    command = input("Reveal or flag a tile? ")
    if command.lower() == 'reveal':
        row = input("Which row? (0 - " + str(board.size - 1) + ") ")
        col = input("Which column? (0 - " + str(board.size - 1) + ") ")
        if validate_square(row, col):
            if not board.left_click(int(row), int(col)):
                lose(int(row), int(col))
                break
            else:
                print(board)
    elif command.lower() == 'flag':
        row = input("Which row? (0 - " + str(board.size - 1) + ") ")
        col = input("Which column? (0 - " + str(board.size - 1) + ") ")
        if validate_square(row, col):
            board.right_click(int(row), int(col))
            print(board)
