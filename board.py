import random


class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.revealed = False
        self.flagged = False
        self.mine = False
        self.value = 0

    def __str__(self):
        if self.flagged:
            return "F"
        elif not self.revealed:
            return " "
        elif self.mine:
            return "X"
        else:
            return str(self.value)

    def __repr__(self):
        debug_str = f"({self.x}, {self.y})"
        if self.mine:
            debug_str += "M"
        if self.flagged:
            debug_str += "F"
        if self.revealed:
            debug_str += "R"
        debug_str += f" {self.value}"


class Board:
    def __init__(self, size, num_mines):
        self.size = size
        self.num_mines = num_mines
        self.board = [[Square(x, y) for y in range(size)] for x in range(size)]
        self.mines = []
        self._generate_mines()
        self._generate_board()

    def _generate_mines(self) -> None:
        """Generates the mines randomly"""
        for i in range(self.num_mines):
            # Randomly pick a location for the mine
            x = random.randint(0, self.size-1)
            y = random.randint(0, self.size-1)
            # If the location is already a mine, pick a new location
            while (x, y) in self.mines:
                x = random.randint(0, self.size-1)
                y = random.randint(0, self.size-1)
            # Add the mine to the list of mines
            self.mines.append((x, y))

    def _generate_board(self) -> None:
        """Generates the board with mines and values"""
        for x in range(self.size):
            for y in range(self.size):
                if (x, y) in self.mines:
                    self.board[x][y].mine = True
                    self.board[x][y].value = -1
                else:
                    self.board[x][y].value = self._count_mines(x, y)

    def _count_mines(self, x: int, y: int) -> int:
        """Returns the number of mines adjacent to the square"""
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if x + i >= 0 and x + i < self.size and y + j >= 0 and y + j < self.size:
                    if self.board[x+i][y+j].mine:
                        count += 1
        return count

    def _reveal(self, x: int, y: int) -> bool:
        """Returns False if the player clicked on a mine, True otherwise"""
        if self.board[x][y].mine:
            return False
        self.board[x][y].revealed = True
        if self.board[x][y].value == 0:
            self._reveal_neighbors(x, y)
        return True

    def _reveal_neighbors(self, x, y):
        """Recursively reveals neighbors of a square with no adjacent mines"""
        raise NotImplementedError

    def left_click(self, x: int, y: int) -> bool:
        """Returns False if the player clicked on a mine, True otherwise
        Does nothing if the square is already revealed or flagged"""
        if self.board[x][y].revealed:
            return True
        if self.board[x][y].flagged:
            return True
        return self._reveal(x, y)

    def right_click(self, x: int, y: int) -> None:
        """Toggles the flagged status of the square"""
        self.board[x][y].flagged = not self.board[x][y].flagged
