"""UI components for the Tic-Tac-Toe game using Pygame."""

import time

import pygame

from constants import (
    BLACK,
    BOARD_SIZE,
    CELL_HEIGHT,
    CELL_WIDTH,
    DIAGONAL_LINE_COLOR,
    FONT_SIZE,
    FPS,
    GAME_DRAW,
    GAME_WON,
    LINE_COLOR,
    LINE_WIDTH,
    O_IMAGE,
    STATUS_BAR_HEIGHT,
    STATUS_Y_POSITION,
    SYMBOL_OFFSET,
    SYMBOL_SIZE,
    TOTAL_HEIGHT,
    WELCOME_IMAGE,
    WHITE,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
    WINNING_LINE_COLOR,
    WINNING_LINE_WIDTH,
    X_IMAGE,
)
from game_logic import TicTacToe


class GameUI:
    """Handles all UI operations for the Tic-Tac-Toe game."""

    def __init__(self) -> None:
        """Initialize the game UI."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, TOTAL_HEIGHT), 0, 32)
        pygame.display.set_caption("Tic Tac Toe")

        # Load and scale images
        self._load_images()

        # Initialize font
        self.font = pygame.font.Font(None, FONT_SIZE)

    def _load_images(self) -> None:
        """Load and scale all game images."""
        self.welcome_image = pygame.image.load(WELCOME_IMAGE)
        self.x_image = pygame.image.load(X_IMAGE)
        self.o_image = pygame.image.load(O_IMAGE)

        # Scale images
        self.x_image = pygame.transform.scale(self.x_image, SYMBOL_SIZE)
        self.o_image = pygame.transform.scale(self.o_image, SYMBOL_SIZE)
        self.welcome_image = pygame.transform.scale(
            self.welcome_image,
            (WINDOW_WIDTH, TOTAL_HEIGHT),
        )

    def show_welcome_screen(self) -> None:
        """Display the welcome screen."""
        self.screen.blit(self.welcome_image, (0, 0))
        pygame.display.update()
        time.sleep(1)

    def draw_board(self) -> None:
        """Draw the game board grid."""
        self.screen.fill(WHITE)

        # Draw vertical lines
        for i in range(1, BOARD_SIZE):
            x_pos = i * CELL_WIDTH
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (x_pos, 0),
                (x_pos, WINDOW_HEIGHT),
                LINE_WIDTH,
            )

        # Draw horizontal lines
        for i in range(1, BOARD_SIZE):
            y_pos = i * CELL_HEIGHT
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (0, y_pos),
                (WINDOW_WIDTH, y_pos),
                LINE_WIDTH,
            )

    def draw_symbols(self, game: TicTacToe) -> None:
        """Draw X and O symbols on the board."""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                symbol = game.board[row][col]
                if symbol is not None:
                    x_pos = col * CELL_WIDTH + SYMBOL_OFFSET
                    y_pos = row * CELL_HEIGHT + SYMBOL_OFFSET

                    if symbol == "x":
                        self.screen.blit(self.x_image, (x_pos, y_pos))
                    else:  # symbol == "o"
                        self.screen.blit(self.o_image, (x_pos, y_pos))

    def draw_winning_line(self, game: TicTacToe) -> None:
        """Draw the winning line if there's a winner."""
        winning_line = game.get_winning_line()
        if winning_line is None:
            return

        line_type, index = winning_line

        if line_type == "row":
            # Horizontal line
            y_pos = (index + 1) * CELL_HEIGHT - CELL_HEIGHT // 2
            pygame.draw.line(
                self.screen,
                WINNING_LINE_COLOR,
                (0, y_pos),
                (WINDOW_WIDTH, y_pos),
                WINNING_LINE_WIDTH,
            )
        elif line_type == "col":
            # Vertical line
            x_pos = (index + 1) * CELL_WIDTH - CELL_WIDTH // 2
            pygame.draw.line(
                self.screen,
                WINNING_LINE_COLOR,
                (x_pos, 0),
                (x_pos, WINDOW_HEIGHT),
                WINNING_LINE_WIDTH,
            )
        elif line_type == "diagonal_main":
            # Main diagonal (top-left to bottom-right)
            pygame.draw.line(
                self.screen,
                DIAGONAL_LINE_COLOR,
                (50, 50),
                (WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50),
                WINNING_LINE_WIDTH,
            )
        elif line_type == "diagonal_anti":
            # Anti-diagonal (top-right to bottom-left)
            pygame.draw.line(
                self.screen,
                DIAGONAL_LINE_COLOR,
                (WINDOW_WIDTH - 50, 50),
                (50, WINDOW_HEIGHT - 50),
                WINNING_LINE_WIDTH,
            )

    def draw_status(self, game: TicTacToe) -> None:
        """Draw the game status message."""
        if game.game_state == GAME_WON and game.winner:
            message = f"{game.winner.upper()} won!"
        elif game.game_state == GAME_DRAW:
            message = "Game Draw!"
        else:
            message = f"{game.current_player.upper()}'s Turn"

        text = self.font.render(
            message,
            True,
            WHITE,
        )

        # Clear status area
        self.screen.fill(BLACK, (0, WINDOW_HEIGHT, WINDOW_WIDTH, STATUS_BAR_HEIGHT))

        # Center the text
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, STATUS_Y_POSITION))
        self.screen.blit(text, text_rect)

    def get_clicked_cell(self, mouse_pos: tuple[int, int]) -> tuple[int, int] | None:
        """Convert mouse position to board cell coordinates.

        Args:
            mouse_pos: Tuple of (x, y) mouse coordinates

        Returns:
            Tuple of (row, col) or None if click is outside the board

        """
        x, y = mouse_pos

        # Check if click is within the game board
        if x < 0 or y < 0 or x >= WINDOW_WIDTH or y >= WINDOW_HEIGHT:
            return None

        col = x // CELL_WIDTH
        row = y // CELL_HEIGHT

        # Ensure we don't go beyond board boundaries due to rounding
        if row >= BOARD_SIZE or col >= BOARD_SIZE:
            return None

        return (row, col)

    def update_display(self) -> None:
        """Update the display."""
        pygame.display.update()

    def tick(self) -> None:
        """Tick the game clock."""
        self.clock.tick(FPS)

    def quit(self) -> None:
        """Quit pygame."""
        pygame.quit()
