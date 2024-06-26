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
            return "\u2588"
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
        return debug_str


class Board:
    def __init__(self, size: int, num_mines: int):
        """Initializes the board with the given size (n x n) and number of mines"""
        self.size = size
        self.num_mines = num_mines
        self.board = [[Square(x, y) for y in range(size)] for x in range(size)]
        self.mines = []
        self._generate_mines()
        self._generate_board()
        self.num_revealed = 0

    def __str__(self):
        vis_board = ""
        for x in range(self.size):
            for y in range(self.size):
                vis_board += str(self.board[x][y]) + " "
            vis_board += "\n"
        return vis_board

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
                    if (x + i, y + j) in self.mines:
                        count += 1
        return count

    def _reveal_neighbors(self, x: int, y: int) -> bool:
        """Recursively reveals neighbors of a square with no adjacent mines
        Check if current square is a mine, if so, return False
        Check if current square is already revealed, if so, return True
        Check if current square is flagged, if so, return True
        Set current square to revealed
        If current square has adjacent mines, return True to stop recursion
        Recursively reveal neighbors of the current square
        """
        ret_val = True
        if self.board[x][y].revealed:
            return True
        self.board[x][y].revealed = True
        self.num_revealed += 1  # advances toward win condition
        if self.board[x][y].mine:
            return False
        if self.board[x][y].flagged:
            return True
        if self.board[x][y].value != 0:
            return True
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i in range(self.size) and j in range(self.size):
                    ret_val = self._reveal_neighbors(i, j) and ret_val
        return ret_val

    def left_click(self, x: int, y: int) -> bool:
        """Returns False if the player clicked on a mine, True otherwise
        Does nothing if the square is already flagged
        Runs chord function if the square is already revealed"""
        if self.board[x][y].revealed:
            return self._chord(x, y)
        if self.board[x][y].flagged:
            return True
        return self._reveal_neighbors(x, y)

    def right_click(self, x: int, y: int) -> None:
        """Toggles the flagged status of the square"""
        self.board[x][y].flagged = not self.board[x][y].flagged

    def _count_flags(self, x: int, y: int) -> bool:
        """Checks if there are adjacent flags >= the number of adjacent mines"""
        flag_count = 0
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i in range(self.size) and j in range(self.size):
                    if self.board[i][j].flagged:
                        flag_count += 1
        if flag_count >= self.board[x][y].value:
            return True
        return False

    def _chord(self, x: int, y: int) -> bool:
        """Reveals adjacent non-flagged tiles if enough are flagged"""
        ret_val = True
        if self._count_flags(x, y):
            for i in range(x - 1, x + 2):
                for j in range(y - 1, y + 2):
                    if i in range(self.size) and j in range(self.size):
                        if not self.board[i][j].flagged:
                            ret_val = self._reveal_neighbors(i, j) and ret_val
        return ret_val
