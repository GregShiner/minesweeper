import pygame
from board import Board, Square

# Initialize Pygame
pygame.init()

# Set up the window
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Define colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

# Other constants
SQUARE_SIZE = 40  # Size of each square on the board


def draw_board(board):
    for x in range(board.size):
        for y in range(board.size):
            square = board.board[x][y]
            color = WHITE if square.revealed else GRAY
            pygame.draw.rect(WIN, color, (x * SQUARE_SIZE, y *
                             SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.rect(WIN, BLACK, (x * SQUARE_SIZE, y *
                             SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 1)
            if square.revealed:
                # Draw number of mines around the square if it's not a mine
                if not square.mine and square.value > 0:
                    font = pygame.font.SysFont(None, 30)
                    text = font.render(str(square.value), True, BLACK)
                    text_rect = text.get_rect(
                        center=(x * SQUARE_SIZE + SQUARE_SIZE // 2, y * SQUARE_SIZE + SQUARE_SIZE // 2))
                    WIN.blit(text, text_rect)
                # Draw mine if it's a mine
                elif square.mine:
                    pygame.draw.circle(
                        WIN, BLACK, (x * SQUARE_SIZE + SQUARE_SIZE // 2, y * SQUARE_SIZE + SQUARE_SIZE // 2), 10)
            elif square.flagged:
                font = pygame.font.SysFont(None, 30)
                text = font.render("F", True, BLACK)
                text_rect = text.get_rect(
                    center=(x * SQUARE_SIZE + SQUARE_SIZE // 2, y * SQUARE_SIZE + SQUARE_SIZE // 2))
                WIN.blit(text, text_rect)


def main():
    # Initialize board
    board = Board(size=10, num_mines=10)
    lost = False  # Flag to track if the player has lost
    won = False

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:  # Left mouse button
                    # Calculate which square was clicked
                    x, y = pygame.mouse.get_pos()
                    x //= SQUARE_SIZE
                    y //= SQUARE_SIZE
                    # Left click on the square if within bounds and not already lost
                    if 0 <= x < board.size and 0 <= y < board.size and not lost:
                        if not board.left_click(x, y):  # If left click on a mine
                            lost = True
                        elif board.num_revealed + board.num_mines == board.size * board.size:
                            won = True
                elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                    # Calculate which square was clicked
                    x, y = pygame.mouse.get_pos()
                    x //= SQUARE_SIZE
                    y //= SQUARE_SIZE
                    # Right click on the square if within bounds and not already lost
                    if 0 <= x < board.size and 0 <= y < board.size and not lost:
                        board.right_click(x, y)

        # Draw the board
        WIN.fill(WHITE)
        draw_board(board)

        # Check if the player has lost
        if lost:
            font = pygame.font.SysFont(None, 50)
            text = font.render("You Lost!", True, (255, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            WIN.blit(text, text_rect)
        elif won:
            font = pygame.font.SysFont(None, 50)
            text = font.render("You Won!", True, (0, 0, 255))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            WIN.blit(text, text_rect)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()

