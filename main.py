import pygame
from board import Board

# Initialize Pygame
pygame.init()

# Set up the window
GRID_WIDTH, GRID_HEIGHT = 400, 400  # Width and height of the grid
BORDER_WIDTH = 10  # Width of the border around the grid
WINDOW_WIDTH = GRID_WIDTH + BORDER_WIDTH * 2
# Add space for the timer, mine counter, and name
WINDOW_HEIGHT = GRID_HEIGHT + 160
WIN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Minesweeper")

# Define colors
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Other constants
SQUARE_SIZE = 40  # Size of each square on the board
FONT_SIZE = 20  # Font size for text
TIMER_POSITION = (10, 10)  # Position of the timer
MINE_COUNTER_POSITION = (WINDOW_WIDTH - 10, 10)  # Position of the mine counter
NAME_POSITION = (WINDOW_WIDTH // 2, 50)  # Position of the name
# Position of the win/lose message
WIN_LOSE_POSITION = (WINDOW_WIDTH // 2, 100 + GRID_HEIGHT // 2)


def draw_board(board):
    # Draw border around the grid
    pygame.draw.rect(WIN, BLACK, (BORDER_WIDTH, 100,
                     GRID_WIDTH, GRID_HEIGHT), BORDER_WIDTH)

    for x in range(board.size):
        for y in range(board.size):
            square = board.board[x][y]
            color = WHITE if square.revealed else GRAY
            pygame.draw.rect(WIN, color, (x * SQUARE_SIZE + BORDER_WIDTH, y *
                             SQUARE_SIZE + 100, SQUARE_SIZE, SQUARE_SIZE))  # Adjust x and y positions
            pygame.draw.rect(WIN, BLACK, (x * SQUARE_SIZE + BORDER_WIDTH, y *
                             SQUARE_SIZE + 100, SQUARE_SIZE, SQUARE_SIZE), 1)  # Adjust x and y positions
            if square.revealed:
                if square.mine:
                    pygame.draw.circle(
                        WIN, BLACK, (x * SQUARE_SIZE + SQUARE_SIZE // 2 + BORDER_WIDTH, y * SQUARE_SIZE + SQUARE_SIZE // 2 + 100), 10)  # Adjust x and y positions
                elif square.value > 0:
                    font = pygame.font.SysFont(None, FONT_SIZE)
                    text = font.render(str(square.value), True, BLACK)
                    text_rect = text.get_rect(
                        center=(x * SQUARE_SIZE + SQUARE_SIZE // 2 + BORDER_WIDTH, y * SQUARE_SIZE + SQUARE_SIZE // 2 + 100))  # Adjust x and y positions
                    WIN.blit(text, text_rect)

            elif square.flagged:
                font = pygame.font.SysFont(None, FONT_SIZE)
                text = font.render("F", True, RED)
                text_rect = text.get_rect(
                    center=(x * SQUARE_SIZE + SQUARE_SIZE // 2 + BORDER_WIDTH, y * SQUARE_SIZE + SQUARE_SIZE // 2 + 100))  # Adjust x and y positions
                WIN.blit(text, text_rect)


def display_result(message, color):
    font = pygame.font.SysFont(None, 50)
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=WIN_LOSE_POSITION)
    WIN.blit(text, text_rect)


def main():
    # Initialize board
    board = Board(size=10, num_mines=10)
    lost = False  # Flag to track if the player has lost
    won = False   # Flag to track if the player has won
    game_over = False  # Flag to track if the game is over

    # Timer variables
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    elapsed_time = 0

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not game_over:
                    if pygame.mouse.get_pressed()[0]:  # Left mouse button
                        x, y = pygame.mouse.get_pos()
                        # Adjust x position
                        x = (x - BORDER_WIDTH) // SQUARE_SIZE
                        y = (y - 100) // SQUARE_SIZE  # Adjust y position
                        if 0 <= x < board.size and 0 <= y < board.size:
                            # If left click on a mine
                            if not board.left_click(x, y):
                                lost = True
                                game_over = True
                            elif board.num_revealed + board.num_mines == board.size * board.size:
                                won = True
                                game_over = True
                    elif pygame.mouse.get_pressed()[2]:  # Right mouse button
                        x, y = pygame.mouse.get_pos()
                        # Adjust x position
                        x = (x - BORDER_WIDTH) // SQUARE_SIZE
                        y = (y - 100) // SQUARE_SIZE  # Adjust y position
                        if 0 <= x < board.size and 0 <= y < board.size:
                            board.right_click(x, y)

        # Update timer
        if not game_over:
            elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        # Draw the board
        WIN.fill(WHITE)
        draw_board(board)

        # Display timer
        font = pygame.font.SysFont(None, FONT_SIZE)
        timer_text = font.render(f"Time: {elapsed_time}", True, BLACK)
        timer_rect = timer_text.get_rect(topleft=TIMER_POSITION)
        WIN.blit(timer_text, timer_rect)

        # Display mine counter
        mines_remaining = board.num_mines - \
            sum(square.flagged for row in board.board for square in row)
        mine_counter_text = font.render(
            f"Mines: {mines_remaining}", True, BLACK)
        mine_counter_rect = mine_counter_text.get_rect(
            topright=MINE_COUNTER_POSITION)
        WIN.blit(mine_counter_text, mine_counter_rect)

        # Display game name
        font = pygame.font.SysFont(None, 50)
        name_text = font.render("Minesweeper", True, BLACK)
        name_rect = name_text.get_rect(center=NAME_POSITION)
        WIN.blit(name_text, name_rect)

        # Display game result
        if game_over:
            if lost or won:
                display_result("You Lose!" if lost else "You Win!",
                               RED if lost else BLUE)

        pygame.display.update()
        clock.tick(30)  # Cap the frame rate at 30 FPS

    pygame.quit()


if __name__ == "__main__":
    main()
